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
            <input type="password" placeholder="请输入密码"  v-model="password">
          </div>
          <div class="btnBox">
            
            <button type="button" class="submitBtn" @click="submitLogin">
                <span>立即登录</span>
            </button>
         
          </div>
          
        </form>
</template>

<script scoped>
import http from "../../shared/Http.js";

export default {
    name:"LoginForm",
    data(){
      return{
        name:'',
        password:'',

      }
    },
    methods:{
      
      async submitLogin() {
        const response = await http
          .post(
            "/login",
            {
              params: { name:this.name, password:this.password},
            },
            {
              headers: {
                //头部参数
                "Content-Type": "application/json",
              },
            }
          )
          .catch((error) => {console.log(error);this.$message.error("登录失败");});
          
      if (response.status === 200) {
        this.$message({
          message: "登录成功",
          type: "success",
          
        });
        this.$router.push({
          name: `main`, // 只是把query改了，其他都没变
        });
        window.location.reload();
      } 
      localStorage.removeItem('user');
      localStorage.setItem("user",JSON.stringify(response["data"]['user'][0]))
    },
    }
}
</script>

<style>
form{
    margin-top: 45px;
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