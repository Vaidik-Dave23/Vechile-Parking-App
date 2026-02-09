import {createWebHistory, createRouter} from 'vue-router';
import Content from './components/Content.vue'
import LoginPage from './components/LoginPage.vue'
import RegisterPage from './components/RegisterPage.vue'
import Dashboard from './components/Dashboard.vue';
import Profile from './components/Profile.vue';
import UpdateProfile from './components/UpdateProfile.vue';

import AddParkingLots from './components/AddParkingLots.vue';
import ParkingLotUpdate from './components/ParkingLotUpdate.vue';
import Users from './components/Users.vue';
import Reservations from './components/Reservations.vue';
import AdminSearch from './components/AdminSearch.vue';
import AdminSummary from './components/AdminSummary.vue';

import Reserve from './components/Reserve.vue';
import Release from './components/Release.vue';
import Search from './components/Search.vue';
import UserSummary from './components/UserSummary.vue';
const routes=[
    {path: '/', component: Content },
    {path: '/login', component:LoginPage},
    {path: '/register', component: RegisterPage},
    {path: '/dashboard', component: Dashboard},
    {path: '/profile', component: Profile},
    {path: '/profile/update', component: UpdateProfile},

    {path: '/admin/parkinglot', component: AddParkingLots},
    {path:'/admin/parkinglots/:lot_id', component: ParkingLotUpdate},
    {path:'/admin/users', component: Users},
    {path:'/admin/reservations', component: Reservations},
    {path: '/admin/search', component: AdminSearch},
    {path:'/admin/summary', component: AdminSummary},

    {path:'/user/reserve', component: Reserve},
    {path:'/user/release/:id', component: Release},
    {path:'/user/search', component: Search},
    {path:'/user/summary',component: UserSummary},]

export const router = createRouter({
    history: createWebHistory(),
    routes
});
