# blog_api 下的 urls
from django.urls import path
from . import views

# 必须加上，且同 project 下 urls 中的 namespace 同值
app_name = 'api'

urlpatterns = [

    path(r'adminlogin', views.adminLogin, name="api_posts"),

    path(r'login', views.userLogin, name="api_posts"),
    path(r'register', views.userRegister, name="api_posts"),
    path(r'changePwd', views.userChangePwd, name="api_posts"),
    path(r'getall', views.adminGetAll, name="api_posts"),

    path(r'createOrderInfo', views.createOrderInfo, name="api_posts"),
    path(r'createOrder', views.createOrder, name="api_posts"),
    path(r'orders/pay', views.payorder, name="api_posts"),
    path(r'orders/qianshou', views.qianshouOrder, name="api_posts"),
    path(r'orders/comment', views.commentOrder, name="api_posts"),
    path(r'orders/quxiao', views.userdeleteOrder, name="api_posts"),
    path(r'cargos/getCargos', views.getCargos, name="api_posts"),
    path(r'editCargos', views.user_edit_cargos, name="api_posts"),
    path(r'getmain', views.getMain, name="api_posts"),



    path(r'getOrder', views.getOrder, name="api_posts"),
    path(r'getOrderById', views.getOrderById, name="api_posts"),
    path(r'getDistance', views.getDistance, name="api_posts"),

    path(r'users/', views.post_list, name="api_posts"),
    path(r'users/add', views.addUser, name="users_add"),
    path(r'users/delete', views.deleteUser, name="users_delete"),
    path(r'users/switch', views.switchUser, name="users_switch"),
    path(r'users/edit', views.editUser, name="users_edit"),
    path(r'users/search', views.searchUser, name="users_search"),

    path(r'ports/', views.ports_list, name="api_posts"),
    path(r'ports/add', views.addPort, name="users_add"),
    path(r'ports/delete', views.deletePort, name="users_delete"),
    path(r'ports/edit', views.editPort, name="users_edit"),
    path(r'ports/search', views.searchPort, name="users_search"),

    path(r'ships/', views.ships_list, name="api_posts"),
    path(r'ships/add', views.addShip, name="users_add"),
    # path(r'ships/delete', views.deletePort, name="users_delete"),
    path(r'ships/edit', views.editShip, name="users_edit"),
    path(r'ships/search', views.searchShip, name="users_search"),


    path(r'cargos/', views.cargos_list, name="api_posts"),
    path(r'cargos/add', views.addCargo, name="users_add"),
    path(r'cargos/delete', views.deleteCargo, name="users_delete"),
    path(r'cargos/edit', views.editCargo, name="users_edit"),
    path(r'cargos/search', views.searchCargo, name="users_search"),

    path(r'orders', views.orders_list, name="api_posts"),
    path(r'orders/search', views.searchOrder, name="users_search"),
    path(r'orders/delete', views.deleteOrder, name="users_delete"),

    path(r'task', views.getTask, name="api_posts"),
    path(r'task/desc', views.getTaskDesc, name="api_posts"),

    path(r'fahuo', views.fahuo, name="api_posts"),

]