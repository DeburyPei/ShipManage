<template>
  <div id="Login">
    <div class="background-top">
      <img src="../assets/bgImg/login/login_background_top.png" alt="" />
      <div class="logoAndTitle">
        <img src="../assets/logo/logo.svg" alt="" class="logo" />
        <h1>起航科技</h1>
      </div>
    </div>
    <div class="background-bottom">
      <img src="../assets/bgImg/login/login_background_bottom.png" alt="" />
    </div>
    <div class="login_form">
      <div class="form_left">
        <img
          src="../assets/bgImg/login/login_bg.jpg"
          alt=""
          class="left_back"
        />
        <div class="left_content"></div>
        <div class="left_text">
          <div class="title">
            船舶物流
            <br />
            管理系统
          </div>
          <div class="text_img">
            <img src="../assets/bgImg/login/bolang.png" alt="" />
          </div>
          <div class="text">Leading the future</div>
          <div class="text_img1">
            <img src="../assets/bgImg/login/login_kjhl.png" alt="" />
          </div>
        </div>
      </div>
      <div class="form_right">
        <img src="../assets/logo/login_logo.svg" alt="" class="form_logo" />
        <div v-if="this.isLogin">
            <LoginForm />
        </div>
       <div v-else>
            <RegisterForm />
       </div>
       <div class="huan" @click="changeLogOrReg">去注册</div>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from '../components/login/loginForm.vue'
import RegisterForm from '../components/login/registerForm.vue'


export default {
  name: "Login",
  components:{
    LoginForm,
    RegisterForm
  },
  data(){
    return{
        isLogin: true,
        
    }
  },
  methods:{
    changeLogOrReg(){ 
        this.isLogin = !this.isLogin
        let huan = document.querySelector('.huan')
        if(huan.innerHTML === "去注册"){
            huan.innerHTML = "去登录"
        }else{
            huan.innerHTML = "去注册"
        }
    }
  }
};
</script>

<style scoped>
.logoAndTitle {
  display: flex;
  position: absolute;

  top: 20px;
  left: 65px;
  color: #fff;
}
.logoAndTitle h1 {
  padding-top: 27px;
}
.logo {
  width: 80px;
  height: 100px;
}
.background-top-topck {
  position: absolute;
  top: 0;
}
.background-bottom {
  position: absolute;
  bottom: 0;
  right: 0;
}
.login_form {
  display: flex;
  width: 62.5%;
  height: 500px;
  position: absolute;
  top: 50%;
  left: 50%;
  background: white;
  border-radius: 10px;
  transform: translate(-50%, -50%);
}
.login_form .form_left {
  width: 55%;
  height: 100%;
  position: relative;
}
.left_back {
  height: 100%;
  width: 100%;
  border-radius: 10px 0 0 10px;
}
.left_text {
  width: 220px;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
  padding-left: 44px;
}
.left_content {
  width: 220px;
  height: 100%;
  background: #2a3f54;
  opacity: 0.8;
  border-radius: 10px 0 0 10px;
  position: absolute;
  left: 0;
  top: 0;
}
.title {
  width: 124px;
  height: 64px;
  font-size: 30px;
  font-family: SimSun;
  font-weight: 400;
  color: #fff;
  margin-top: 50px;
}
.text_img {
  width: 57px;
  height: 16px;
  margin-top: 70px;
}
.text {
  width: 107px;
  height: 13px;
  font-size: 12px;
  font-family: Microsoft YaHei;
  font-weight: 400;
  color: #fff;
  margin-top: 20px;
}
.text_img1 {
  width: 130px;
  height: 130px;
  margin-top: 70px;
}
.form_right{
    width: 45%;
    height: 100%;
    text-align: center;
}
.form_logo{
    width: 80px;
    height: 80px;
    
    margin-top: 45px;
}
.huan{
   
    font-size: 16px;
    font-family: Microsoft YaHei;
    font-weight: 400;
    color: #2a3f54;
    cursor: pointer;
    width: 60px;
    margin: 0 auto;
    margin-top: 30px;

}
</style>