from celery import shared_task
import csv
import datetime
import os
from jinja2 import Template
from .mail import send_email
from Backend.application.models import Reservation, User ,Parkinglot
from Backend.application.database import db

@shared_task(ignore_results=False, name='export_reservation_csv')
def export_reservation_csv():
    reservations = Reservation.query.all()

    csv_file_name = f"reservations_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    csv_path = os.path.join("static", csv_file_name)

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Sr No.', 'User Full Name', 'User Email',
            'Parking Lot ID', 'Parking Spot ID',
            'Vehicle Number', 'Start Time', 'End Time', 'Amount Paid'
        ])

        for idx, r in enumerate(reservations, start=1):
            user = User.query.get(r.user_id)
            writer.writerow([
                idx,
                user.full_name if user else 'Unknown',
                user.email_id if user else 'Unknown',
                r.parking_lot_id,
                r.parking_spot_id,
                r.vehicle_number,
                r.start_time,
                r.end_time,
                r.amount_paid
            ])

    return csv_file_name


@shared_task(ignore_results=False, name="monthly_report")
def monthly_report():
    users = User.query.all()
    for user in users[1:]:  
        user_data = {}
        user_data['username'] = user.full_name
        user_data['email'] = user.email_id

   
        now = datetime.datetime.now()
        this_month_reservations = Reservation.query.filter(
            Reservation.user_id == user.id,
            extract('year', Reservation.start_time) == now.year,
            extract('month', Reservation.start_time) == now.month
        ).all()


        details = []
        for res in this_month_reservations:
            info_dict = {}
            lot = Parkinglot.query.get(res.parking_lot_id)
            info_dict["location"] = lot.prime_location_name if lot else "N/A"
            info_dict["start_time"] = res.start_time.strftime('%Y-%m-%d %H:%M')
            info_dict["end_time"] = res.end_time.strftime('%Y-%m-%d %H:%M') if res.end_time else "Not Released"
            info_dict["price"] = res.parking_cost if res.price else "N/A"
            details.append(info_dict)

        user_data['details'] = details


        mail_template = """
        <h3>Dear {{ user_data.username }}</h3>
        <p>Here's your activity report for this month:</p>
        <p>Visit the parking app at http://127.0.0.1:5173 for more.</p>
        <table border="1" cellspacing="0" cellpadding="5">
            <tr>
                <th>Location</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Price</th>
            </tr>
            {% for detail in user_data.details %}
            <tr>
                <td>{{ detail.location }}</td>
                <td>{{ detail.start_time }}</td>
                <td>{{ detail.end_time }}</td>
                <td>{{ detail.price }}</td>
            </tr>
            {% endfor %}
        </table>
        <h5>Regards,<br>
        Vehicle Parking App V2<br>
        IITM BS Degree</h5>
        """
        message = Template(mail_template).render(user_data=user_data)

        send_email(user.email_id, subject="Monthly Parking Report", message=message)

    return "Monthly reports sent"

@shared_task(ignore_results=False, name="daily_reminder_mail")
def daily_reminder_mail():
    users = User.query.all()

    for user in users[1:]:  
        reservations = user.reservations  

        if not reservations:
            mail_template = """
            <h3>Dear {{ user.full_name }},</h3>
            <p>This is a reminder from the Parking System.</p>
            <p>You have not made any reservation yet.</p>
            <p>Please visit <a href="http://127.0.0.1:5173">Vehicle Parking App</a> to book a spot if needed.</p>
            <h5>Regards,<br>Parking App V2<br>IITM BS Degree</h5>
            """

            message = Template(mail_template).render(user=user)
            send_email(user.email_id, subject="Daily Reminder - Parking App", message=message)

    return "Daily reminders sent"


