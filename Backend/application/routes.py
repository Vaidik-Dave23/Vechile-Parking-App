from flask import Blueprint,jsonify ,request ,abort
from flask_jwt_extended import jwt_required, create_access_token,current_user, get_jwt_identity
from Backend.application.models import User, Parkinglot, ParkingSpot, Reservation
from Backend.application.database import db
from functools import wraps
from datetime import datetime
from flask import send_from_directory
# from app import cache


routes = Blueprint('routes', __name__)

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            if not current_user.is_admin and role == 'admin':
                return jsonify("Admin access required"), 403
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper


@routes.route('/login', methods=['POST'])
def login():
    email_id = request.json.get('email_id', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email_id=email_id, password=password).one_or_none()
    if not user or not user.password == password:
        
        return jsonify(message="Wrong email or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token), 200

@routes.route('/register', methods=['POST'])
def register():
    print("Request JSON:", request.json)
    email_id = request.json.get('email_id', None)
    password = request.json.get('password', None)
    full_name = request.json.get('full_name', None)
    address = request.json.get('address', None)
    pincode = request.json.get('pincode', None)

    if not email_id or not password or not full_name or not address or not pincode:
        return jsonify({"error": "All fields are required"}), 400
    if User.query.filter_by(email_id=email_id).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(email_id=email_id, password=password, full_name=full_name, address=address, pincode=pincode)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful. Please login."}), 201


@routes.route('/dashboard', methods=['GET'])
# @cache.cached(timeout=60)
@jwt_required()
def dashboard():
    if current_user.is_admin:
        parkinglots = Parkinglot.query.all()


        result = []
        for lot in parkinglots:
            total_spots = len(lot.spots)
            available_spots = sum(1 for spot in lot.spots if spot.is_available)
            result.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,
                'address': lot.address,
                'pincode': lot.pincode,
                'number_of_spots': total_spots,
                'available_spots': available_spots
            })


        return jsonify({
            "role":"admin",
            "email_id": current_user.email_id,
            "full_name": current_user.full_name,
            "parkinglots": result
        }), 200
    else:
        email_id = get_jwt_identity()
        user = User.query.filter_by(email_id=email_id).one_or_none()
        if not user:
            return jsonify({"error": "User not found"}), 404

        reservations = (
            db.session.query(Reservation)
            .filter_by(user_id=user.id)
            .join(ParkingSpot)
            .join(Parkinglot)
            .all()
        )

        parking_history = []
        for res in reservations:
            lot = res.parking_spot.lot
            parking_history.append({
                "id": res.id,
                "location": lot.prime_location_name,
                "vehicle_no": res.vehicle_number,
                "timestamp": res.end_time.strftime("%Y-%m-%d %H:%M:%S") if res.end_time else "",
                "status": "Parked Out" if res.end_time else "Release"
            })

        return jsonify({
            "role":"user",
            "email_id": current_user.email_id,
            "full_name": current_user.full_name,
            "user_name": user.full_name,
            "parking_history": parking_history
        }), 200

        

@routes.route('/admin/parkinglot', methods=['POST'])
@role_required('admin')
def create_parking_lot():
    data = request.get_json()
    prime_location_name = data.get('prime_location_name')
    price = data.get('price')
    address = data.get('address')
    pincode = data.get('pincode')
    number_of_spots = data.get('number_of_spots')

    if not all([prime_location_name, price, address, pincode, number_of_spots]):
        return jsonify({'message': 'All fields are required'}), 400

    lot = Parkinglot(
        prime_location_name=prime_location_name,
        price=price,
        address=address,
        pincode=pincode,
        number_of_spots=number_of_spots
    )
    db.session.add(lot)
    db.session.flush() 

    for _ in range(number_of_spots):
        db.session.add(ParkingSpot(parkinglot_id=lot.id))

    db.session.commit()
    return jsonify({'message': 'Parking lot created successfully'}), 201


    

@routes.route('/admin/parkinglots/<int:lot_id>', methods=['GET'])
@role_required('admin')
def get_parking_lot(lot_id):
    lot = Parkinglot.query.get(lot_id)
    if not lot:
        return jsonify({'error': 'Parking lot not found'}), 404

    return jsonify({
        'id': lot.id,
        'address': lot.address,
        'pincode': lot.pincode,
        'prime_location_name': lot.prime_location_name,
        'number_of_spots': lot.number_of_spots,
        'price': lot.price
    }), 200

@routes.route('/admin/parkinglots/<int:parkinglot_id>', methods=['PUT'])
@role_required('admin')
def update_parking_lot(parkinglot_id):
    lot = Parkinglot.query.get(parkinglot_id)
    if not lot:
        return jsonify({'error': 'Parking lot not found'}), 404

    data = request.get_json()
    lot.prime_location_name = data.get('prime_location_name', lot.prime_location_name)
    lot.address = data.get('address', lot.address)
    lot.pincode = data.get('pincode', lot.pincode)
    lot.price = data.get('price', lot.price)

    new_count = data.get('number_of_spots', lot.number_of_spots)
    current_spots = ParkingSpot.query.filter_by(parkinglot_id=parkinglot_id).all()
    current_count = len(current_spots)

    if new_count > current_count:
        for _ in range(new_count - current_count):
            db.session.add(ParkingSpot(parkinglot_id=parkinglot_id, is_available=True))
    elif new_count < current_count:
        deletable_spots = []
        for spot in current_spots:
            reservation = Reservation.query.filter_by(parking_spot_id=spot.id).first()
            if not reservation:
                deletable_spots.append(spot)
        if len(deletable_spots) < current_count - new_count:
            return jsonify({'error': f'Only {len(deletable_spots)} unreserved spots can be deleted'}), 400
        for spot in deletable_spots[:current_count - new_count]:
            db.session.delete(spot)

    lot.number_of_spots = new_count
    db.session.commit()

    return jsonify({'message': 'Parking lot updated'}), 200





@routes.route('/admin/parkinglots/<int:lot_id>', methods=['DELETE'])
@role_required('admin')
def delete_parkinglot(lot_id):
    lot = Parkinglot.query.get(lot_id)
    if not lot:
        return jsonify({'message': 'Parking lot not found'}), 404

    occupied_spots = ParkingSpot.query.filter_by(parkinglot_id=lot.id, is_available=False).count()
    if occupied_spots > 0:
        return jsonify({'message': 'Cannot delete. Some spots are still occupied.'}), 400

    db.session.delete(lot)
    db.session.commit()
    return jsonify({'message': 'Parking lot deleted successfully'}), 200

@routes.route('/admin/users', methods=['GET'])
@role_required('admin')
def get_all_users():
    users = User.query.filter_by(is_admin=False).all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email_id,
            "address": user.address,
            "pincode": user.pincode
        })

    return jsonify(result), 200

@routes.route('/admin/reservations', methods=['GET'])
@role_required('admin')
def view_reservations():
    reservations = Reservation.query.all()

    result = []
    for res in reservations:
        result.append({
            "id": res.id,
            "user_name": res.user.full_name,
            "email": res.user.email_id,
            "vehicle_number": res.vehicle_number,
            "parking_spot_id": res.parking_spot_id,
            "start_time": res.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": res.end_time.strftime('%Y-%m-%d %H:%M:%S') if res.end_time else None,
            "cost": res.parking_cost
        })

    return jsonify(result), 200


@routes.route('/admin/summary', methods=['GET'])
@role_required('admin')
def admin_summary():
    total_reservations = Reservation.query.count()
    total_revenue = db.session.query(db.func.sum(Reservation.parking_cost)).scalar() or 0

    reservations_by_lot = db.session.query(
        Parkinglot.prime_location_name,
        db.func.count(Reservation.id)
    ).join(ParkingSpot, Parkinglot.id == ParkingSpot.parkinglot_id)\
     .join(Reservation, ParkingSpot.id == Reservation.parking_spot_id)\
     .group_by(Parkinglot.prime_location_name).all()
    
    reservations_by_lot_data = [
        {'lot': lot, 'count': count} for lot, count in reservations_by_lot
    ]

    reservations_by_date = db.session.query(
        db.func.date(Reservation.start_time),
        db.func.count(Reservation.id)
    ).group_by(db.func.date(Reservation.start_time)).all()
    
    reservations_by_date_data = [
        {'date': str(date), 'count': count} for date, count in reservations_by_date
    ]

    return jsonify({
        'total_reservations': total_reservations,
        'total_revenue': total_revenue,
        'reservations_by_lot': reservations_by_lot_data,
        'reservations_by_date': reservations_by_date_data
    })




from flask import request, jsonify
from flask_jwt_extended import jwt_required
from application.database import db
from application.models import User, Parkinglot, ParkingSpot



@routes.route('/admin/search', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_search():
    search_type = request.args.get("type")
    query = request.args.get("query", "").strip().lower()

    if not search_type or not query:
        return jsonify({"error": "Missing search type or query"}), 422

    results = []

    if search_type == "user":
        users = User.query.all()
        for user in users:
            if query in user.full_name.lower() or query in user.email_id.lower():
                results.append({
                    "id": user.id,
                    "full_name": user.full_name,
                    "email_id": user.email_id,
                    "address": user.address,
                    "pincode": user.pincode,
                    "is_admin": user.is_admin
                })

    elif search_type == "location":
        locations = Parkinglot.query.all()
        for loc in locations:
            if query in loc.prime_location_name.lower():
                occupied = ParkingSpot.query.filter_by(parkinglot_id=loc.id, is_available=False).count()
                available = ParkingSpot.query.filter_by(parkinglot_id=loc.id, is_available=True).count()
                results.append({
                    "id": loc.id,
                    "prime_location_name": loc.prime_location_name,
                    "address": loc.address,
                    "pincode": loc.pincode,
                    "price": loc.price,
                    "number_of_spots": loc.number_of_spots,
                    "occupied": occupied,
                    "available": available
                })

    elif search_type == "spot":
        spots = ParkingSpot.query.all()
        for spot in spots:
            if query in str(spot.id) or query in str(spot.parkinglot_id):
                results.append({
                    "id": spot.id,
                    "parkinglot_id": spot.parkinglot_id,
                    "is_available": spot.is_available
                })

    else:
        return jsonify({"error": "Invalid search type"}), 422

    return jsonify({"results": results}), 200




@routes.route('/user/search', methods=['GET','OPTIONS'])
@jwt_required()
def search_parking_lots():
    query = request.args.get('query', '').lower()
    lots = Parkinglot.query.all()

    result = []
    for lot in lots:
        if query in lot.address.lower() or query in lot.pincode or query in lot.prime_location_name.lower():
            available_spots = ParkingSpot.query.filter_by(parkinglot_id=lot.id, is_available=True).count()
            result.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,
                'pincode': lot.pincode,
                'address': lot.address,
                'availability': available_spots
            })

    return jsonify(result), 200


@routes.route('/user/reserve', methods=['POST'])
@jwt_required()
def reserve_parking():
    data = request.json
    lot_id = data.get('lot_id')
    vehicle_number = data.get('vehicle_number')

    email_id = get_jwt_identity() 

    user = User.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    lot = Parkinglot.query.get(lot_id)
    if not lot:
        return jsonify({"message": "Parking lot not found"}), 404

    spot = ParkingSpot.query.filter_by(parkinglot_id=lot_id, is_available=True).first()
    if not spot:
        return jsonify({"message": "No available spots in this lot"}), 400

    spot.is_available = False

    reservation = Reservation(
        user_id=user.id,
        parking_spot_id=spot.id,
        vehicle_number=vehicle_number,
        start_time=datetime.now(),
        end_time=None, 
        parking_cost=0 )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "message": "Reservation successful",
        "spot_id": spot.id,
        "lot_id": lot_id
    }), 201



from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.database import db
from application.models import User, Reservation, ParkingSpot
from datetime import datetime


@routes.route("/release/<int:id>", methods=["POST"])
@jwt_required()
def release_reservation(id):
    email_id = get_jwt_identity()

    user = User.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    if reservation.user_id != user.id:
        return jsonify({"error": "Unauthorized"}), 403

    spot = ParkingSpot.query.get(reservation.parking_spot_id)
    if spot:
        spot.is_available = True

    reservation.end_time = datetime.now()
    db.session.commit()

    return jsonify({"message": "Reservation released successfully"}), 200

@routes.route("/reservations/<int:id>", methods=["GET"])
@jwt_required()
def get_reservation(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    spot = ParkingSpot.query.get(reservation.parking_spot_id)
    if not spot:
        return jsonify({"error": "Spot not found"}), 404

    lot = Parkinglot.query.get(spot.parkinglot_id)
    if not lot:
        return jsonify({"error": "Lot not found"}), 404

    end_time = datetime.now()
    duration_minutes = int((end_time - reservation.start_time).total_seconds() / 60)

    price_per_hour = lot.price or 0
    cost = (duration_minutes / 60) * price_per_hour

    return jsonify({
        "Prime_Location": lot.prime_location_name,
        "address": lot.address,
        "pincode": lot.pincode,
        "Vehicle_Number": reservation.vehicle_number,
        "start_time": str(reservation.start_time),
        "end_time": str(end_time),
        "duration_minutes": duration_minutes,
        "cost": round(cost, 2),
        "price_per_hour": price_per_hour
    })




@routes.route('/user/summary', methods=['GET'])
@role_required('user')
def user_summary():
    email = get_jwt_identity()
    user = User.query.filter_by(email_id=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    total_reservations = Reservation.query.filter_by(user_id=user.id).count()
    total_spent = db.session.query(db.func.sum(Reservation.parking_cost))\
        .filter_by(user_id=user.id).scalar() or 0

    reservations_by_date = db.session.query(
        db.func.date(Reservation.start_time),
        db.func.count(Reservation.id)
    ).filter_by(user_id=user.id)\
     .group_by(db.func.date(Reservation.start_time)).all()

    return jsonify({
        'total_reservations': total_reservations,
        'total_spent': total_spent,
        'reservations_by_date': [
            {"date": str(row[0]), "count": row[1]} for row in reservations_by_date
        ]
    })


@routes.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user = current_user
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "email": user.email_id,
        "full_name": user.full_name,
        "address": user.address,
        "pincode": user.pincode
    }), 200

@routes.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    user = current_user
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json

    if 'email_id' in data and data['email_id'].strip():
        user.email_id = data['email_id']
    if 'full_name' in data and data['full_name'].strip():
        user.full_name = data['full_name']
    if 'address' in data and data['address'].strip():
        user.address = data['address']
    if 'pincode' in data and data['pincode'].strip():
        user.pincode = data['pincode']

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

@routes.route('/admin/parkingspot/<int:spot_id>', methods=['GET'])
@role_required('admin')
def view_parking_spot(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return jsonify({'message': 'Parking spot not found'}), 404

    return jsonify({
        'id': spot.id,
        'is_available': spot.is_available
    }), 200

@routes.route('/admin/parkingspot/<int:spot_id>', methods=['DELETE'])
@role_required('admin')
def delete_parking_spot(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return jsonify({'message': 'Parking spot not found'}), 404

    if not spot.is_available:
        return jsonify({'message': 'Cannot delete. Spot is currently reserved.'}), 400

    db.session.delete(spot)
    db.session.commit()
    return jsonify({'message': 'Parking spot deleted successfully'}), 200

@routes.route('/admin/parkingspot/<int:spot_id>/detail', methods=['GET'])
@role_required('admin')
def parking_spot_detail(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return jsonify({'message': 'Parking spot not found'}), 404

    if spot.is_available:
        return jsonify({'message': 'Parking spot is currently available'}), 200

    reservation = Reservation.query.filter_by(parking_spot_id=spot_id, end_time=None).first()
    if not reservation:
        return jsonify({'message': 'No active reservation found for this spot'}), 404

    return jsonify({
       'spot_id': spot.id,
       'user_id': reservation.user_id,
       'user_name': reservation.user.full_name,
       'vehicle_number': reservation.vehicle_number,
       'reservation_id': reservation.id,
       'start_time': reservation.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        }), 200







from celery.result import AsyncResult
from .tasks import export_reservation_csv,monthly_report,daily_reminder_mail
@routes.route('/export_csv',methods=['GET'])
def exports():
    result=export_reservation_csv.delay()
    return {
        "id":result.id,
        "result":result.result
    }

@routes.route('/api/csv_result/<id>')
def csv_result(id):
    res = AsyncResult(id)
    return send_from_directory('static', res.result)

@routes.route('/api/send_mail/monthly')
def send_mail_monthly():
    res = monthly_report.delay()
    return {
        "message": res.result
    }

@routes.route('/api/send_mail/daily')
def send_mail_daily():
    res = daily_reminder_mail.delay()
    return {
        "message": res.result
    }