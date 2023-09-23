<template>
  <form>
          <div class="form_item">
            <span class="svg-container"
              ><img src="../../assets/bgImg/login/login_user.png" alt="" 
            /></span>
            <input type="text" placeholder="请输入账号" v-model="name">
          </div>
          <div class="form_item">
            <span class="svg-container"
              >
              <img src="../../assets/bgImg/login/login_pwd.png" alt=""
              
            /></span>
            <input  placeholder="请输入手机号" v-model="phone">
          </div>
          <div class="form_item">
            <span class="svg-container"
              >
              <img src="../../assets/bgImg/login/login_pwd.png" alt=""
            /></span>
            
            <input type="password" placeholder="请输入密码"  v-model="password">
          </div>
          <div class="form_item">
            <span class="svg-container"
              >
              <img src="../../assets/bgImg/login/login_pwd.png" alt=""
            /></span>
            <input type="password" placeholder="请再次输入密码"  v-model="againPassword">
          </div>
          <div class="btnBox">
            <button type="button" class="submitBtn" @click="submitRegister">
                <span>立即注册</span>
            </button>
          </div>
          
        </form>
</template>

<script>
import http from "../../shared/Http.js";

export default {
    name:"RegisterForm",
    data(){
      return{
        name:'',
        phone:'',
        password:'',
        againPassword:'',

      }
    },
    methods:{
      
      async submitRegister() {
          if(this.password !== this.againPassword) {
            this.$message.error("两次密码输入不一致")
            return
          }
      const response = await http
        .post(
          "/register",
          {
            params: { name:this.name, password:this.password,phone:this.phone},
          },
          {
            headers: {
              //头部参数
              "Content-Type": "application/json",
            },
          }
        )
        .catch((error) => {console.log(error);this.$message.error("注册失败");});
        console.log(response.status)
      if (response.status === 200) {
        this.$message({
          message: "注册成功",
          type: "success",
        });
        
      } 
      
    },
    }
}
</script>

<style scoped>
form{
    margin-top: 25px;
}
.form_item{
    width: 240px;
    height: 55px;
    line-height: 55px;
    border-bottom: 1px solid #999;
    margin: 0 auto;
    position: relative;
}
.form_item input{
    width: 150px;
    height: 40px;
    outline: none;
    border: none;
    font-size: 18px;
}
.svg-container{
    display: inline-block;
    width: 21px;
    height: 21px;
    position: absolute;
    top: 3px;
    left: 16px;
}
.submitBtn{

    width: 150px;
    height: 50px;
    background: #2a3f54;
    -webkit-box-shadow: 0 7px 22px 0 rgb(42 63 84 / 49%);
    box-shadow: 0 7px 22px 0 rgb(42 63 84 / 49%);
    border-radius: 30px;
    font-size: 22px;
    font-family: Microsoft YaHei;
    font-weight: 400;
    color: #fff;
    outline: none;
    border: none;
    margin-top: 20px;
    cursor: pointer;

}
</style>