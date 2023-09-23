<template>
    <div>
      <div class="navbar">
            <div class="logoAndTitle">
                <img src="../../assets/logo/logo.svg" alt="" class="logo" />
                <h2>起航科技</h2>

                <router-link to="/main">
                    <span>首页</span>
                </router-link>
                
                <router-link to="/main/order">
                    <span>我的订单</span>
                </router-link>
                <router-link to="/main/cargo">
                    <span>我的货物</span>
                </router-link>
                
            </div>
            
            
        <el-dropdown>
          <span class="el-dropdown-link">
               <div class="right-menu" @click='isProfieMenu=!isProfieMenu'>
          <img src="../../assets/bgImg/dashboard/profile_pic.png" alt="" />
          <span class="user-name">{{ this.userInfo['name'] }}</span>
          <i class="el-icon-arrow-down el-icon--right"></i>
        
          
        </div>
          </span>
          <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>首页</el-dropdown-item>
              <el-dropdown-item @click.native="dialogFormVisible=true">修改密码</el-dropdown-item>
              <el-dropdown-item divided @click.native="exitLogin">退出登录</el-dropdown-item>
             
          </el-dropdown-menu>
          </el-dropdown>
       
        <el-dialog title="修改密码" :visible.sync="dialogFormVisible" width="40%"  >
              <el-form >
                  <el-form-item label="旧密码" >
                      <el-input type="password" v-model="ruleForm.oldPass" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="新密码" >
                      <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="再输入新密码" >
                      <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item style="display: flex;justify-content: flex-end;margin-top: 10px;">
                      <el-button type="primary" @click="changePwd">提交</el-button>
                      <el-button @click="resetForm('ruleForm')">重置</el-button>
                  </el-form-item>
              </el-form>
          </el-dialog>
      </div>
    </div>
  </template>
  
  <script>
import http from "../../shared/Http.js";
  
  export default {
    name: "Header",
    data(){
      return{
        userInfo:{},
          isProfieMenu: false,
          dialogFormVisible:false,
          ruleForm: {
            user_id: "",
              oldPass:'',
            pass: '',
            checkPass: '',
          
          }
      }
      
    },
    beforeMount(){
      this.userInfo = JSON.parse(localStorage.getItem('user'))
      this.ruleForm.user_id = this.userInfo["id"]
    },
    methods:{
     
      async changePwd(formName) {
          if(this.ruleForm.checkPass !== this.ruleForm.pass){
            this.$message.error("两次密码不一致");
            return
          }
        const response = await http
            .post("/changePwd",
            {
              params: this.ruleForm ,
            })
            .catch((error) => console.log(error));
            if (response.status === 200) {
              this.$message({
                message: "修改密码成功",
                type: "success",
              });
            } 
            else{
              this.$message.error("修改密码失败");

            }
        },
        resetForm(formName) {
           Object.assign(this.ruleForm,{
              oldPass:'',
            pass: '',
            checkPass: '',
          
          })
        },
        exitLogin(){
          localStorage.removeItem('user');
          this.$router.push("/");
        }
      
    }
  };
  </script>
      
  <style scoped>
  .logoAndTitle a{
    margin-right: 50px;
    color: black;
  
  }
  h2{
    margin-right: 100px;
  }
  .logoAndTitle a:hover{
    border-bottom: 2px solid blue;
  
  }
  .navbar {
    background:#fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
    /* margin-top: 10px; */
  }
  .right-menu img {
    width: 40px;
    height: 40px;
    vertical-align: middle;
  }
  .right-menu {
  margin-right: 10px;
}
  .right-menu span {
    vertical-align: middle;
    font-size: 12px;
    margin-left: 7px;
  }
  /* #dropdown-menu{
      position: absolute;
      top: 36px;
      left: calc(100vw - 133px);
  } */
  .el-form-item{
      margin-bottom: 0;
  }
  .el-form{
      margin-top: 0;
  }
  .el-dialog{
      width: 40%;
  }

  .logoAndTitle{
    display: flex;
   
    position: relative;
    /* width: 100%; */
    height: 50px;
    line-height: 50px;
    /* background: #304156; */
    text-align: center;
    overflow: hidden;
}

  </style>