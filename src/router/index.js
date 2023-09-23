
import Vue from 'vue'
import Router from 'vue-router'
import Login from '../views/Login.vue'
import Main from '../views/Main.vue'
import MainBody from "../components/main/mainBody.vue"
import MyOrder from "../components/main/myOrder.vue"
import OrderAllInfo from "../components/main/orderAllInfo.vue"
import MyCargo from "../components/main/myCargo.vue"
import CargoEdit from "../components/main/cargoEdit.vue"



Vue.use(Router)
const routes = [
    {
        name:'root',
        path: '/',
        component:Login
    },
    {
        name:'main',
        path: '/main',
        component:Main,
        children:[
            {
                path: '',
                component: MainBody,
               
              },
              {
                path: 'order',
                component: MyOrder,
               
              },
              {
                path: 'orderallinfo',
                name:'orderAllInfo',
                component: OrderAllInfo,
               
              },
              {
                path: 'cargo',
                component: MyCargo,
               
              },
              {
                name:"cargoedit",
                path: 'cargoEdit',
                component: CargoEdit,
               
              },
        ]
    },
    
]

const router = new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router