<template>
    <div class="cargo">
        <div class="h11">
      <h1><i class="el-icon-box"></i>修改货物 货物号：{{ this.id }}</h1>
     
    </div>
    <div class="main">
        <el-form
        :model="cargoForm"
        status-icon
        label-width="100px"
        class="demo-ruleForm"
      >
      <el-form-item label="货名" >
                      <el-input  v-model="cargoForm.cargo_name" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="货型" >
                      <el-input  v-model="cargoForm.cargo_type" autocomplete="off"></el-input>
                  </el-form-item>
                
                  <el-form-item label="重量 kg" >
                      <el-input  v-model="cargoForm.weight" autocomplete="off"></el-input>
                  </el-form-item>
                  
                  
                     
        <el-form-item>
          <el-button type="primary" @click="submitForm()">提交</el-button>
          <el-button @click="resetForm()">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
      
    </div>
  </template>
  
  <script>
  import http from "../../shared/Http.js";
  
  export default {
    name: "CargoEdit",
  
    data() {
      return {
        id:"",
        cargoForm:{
              cargo_name:'',
              cargo_type:'',
              weight:'',
            
          },
      };
    },
    async beforeMount() {
      this.id = this.$route.query.id;
      
    },
    methods: {
      async submitForm() {
        
        const response = await http
          .post(
            "/editCargos",
            {
              params: { id: this.id, form: this.cargoForm },
            },
            {
              headers: {
                //头部参数
                "Content-Type": "application/json",
              },
            }
          )
          .catch((error) => console.log(error));
        if (response.status === 200) {
          this.$message({
            message: "恭喜你，这是一条成功消息",
            type: "success",
          });
        } else {
          this.$message.error("错了哦，这是一条错误消息");
        }
      },
      resetForm() {
        Object.assign(this.cargoForm, {
          cargo_name:'',
              cargo_type:'',
              weight:'',
              user_id:''
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .el-input{
    width: 230px;
  }

.h11 {
  display: flex;
  justify-content: space-between;
}
.cargo {
  width: 80%;
  margin: 0 auto;
}
.main{
    margin-top: 50px;
}
  </style>