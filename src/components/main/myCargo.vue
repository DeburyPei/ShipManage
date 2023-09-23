<template>
  <div class="cargo">
    <div class="h11">
      <h1><i class="el-icon-box"></i>我的货物</h1>
      <el-button type="success" round @click="isReadOrWrite = !isReadOrWrite">{{
        buttonText
      }}</el-button>
    </div>
    <div class="main">
        <div class="options" v-if="isReadOrWrite===true">
        <el-table
            :data="tableData"
            border
            style="width: 100%">
            <el-table-column
            prop="id"
            label="货物号"
            align="center"

            width="100">
            </el-table-column>
            <el-table-column
            prop="name"
            label="货名"
            align="center"

            >

            </el-table-column>
            <el-table-column
                prop="type"
                label="货物类型"
               
                align="center"

            >
            
            </el-table-column>
            <el-table-column
            prop="weight"
            label="重量 kg"
            
            align="center"

            >
            
            </el-table-column>
           
            <el-table-column
            prop="status"
            label="是否运输完成"
            
            align="center"

            >
            <template slot-scope="scope">
                 <div v-if="scope.row.status===false">
                
                <el-button type="warning">未完成</el-button>
            </div>
            <div v-else>
                <el-button type="success">已完成</el-button>
            </div>
            </template>
            <!-- <p>{{ status }}</p> -->
           
            </el-table-column>
            <el-table-column label="操作" align="center" width="180">
                <template slot-scope="scope">
                    <el-button
                    size="mini"
                    @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button
                    size="mini"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        </div>
       <div class="options" v-else>
        <el-steps :space="200" :active="steps" finish-status="success">
            <el-step title="添加货物"></el-step>
            <el-step title="完成添加"></el-step>
        </el-steps>
        <div class="form">
            <div v-if="steps===0">
                <el-form >
                    <el-form-item label="货名" >
                            <el-input  v-model="cargoForm.cargo_name" autocomplete="off"></el-input>
                        </el-form-item>
                        <el-form-item label="货型" >
                            <el-input  v-model="cargoForm.cargo_type" autocomplete="off"></el-input>
                        </el-form-item>
                    
                        <el-form-item label="重量 kg" >
                            <el-input  v-model="cargoForm.weight" autocomplete="off"></el-input>
                        </el-form-item>
                        
                       
                        <el-form-item style="">
                            <el-button type="primary" @click="addCargo" style="margin-left: 10vw;margin-top: 10px;">提交</el-button>
                            <el-button @click="resetForm('cargoForm')" >重置</el-button>
                        </el-form-item>
            </el-form>
            </div>
            
            <div v-else-if="steps===1">
                <el-result icon="success" title="完成" subTitle="">
                    <template slot="extra">
                        <el-button type="primary" size="medium" @click="refresh">查看货物</el-button>
                    </template>
                </el-result>
            </div>

          
        </div>
       
      </div>
        </div>
    </div>
 
</template>

<script>
import http from "../../shared/Http.js";

export default {
    name:"MyCargo",
    data() {
        return {
            steps:0,
            isReadOrWrite:true,
            tableData:[] ,
            cargoForm:{
                    cargo_name:'',
                    cargo_type:'',
                    weight:'',
                    user_id:'',
                },
        }
    },
    computed: {
        buttonText() {
        return this.isReadOrWrite ? "添加货物" : "查看货物";
        },
   
  },
  async beforeMount() {
    this.userInfo = JSON.parse(localStorage.getItem('user'))
    
    const response = await http
            .get("/cargos/getCargos",
            {
              params: { user_id:this.userInfo['id'] },
            })
            .catch((error) => console.log(error));
            
            // this.shipOptions = response.data["ships"]
            // this.cargoOptions = response.data["cargos"]
            // this.portOptions = response.data["port"]
            // const orderResponse = await http
            // .get("/getOrder",
            // {
            //   params: { id:this.userInfo['id'] },
            // }).catch((error) => console.log(error));
            this.tableData = response.data
  },
  methods: {
    refresh() {
      window.location.reload();
    },
    handleEdit(index,row){
        this.$router.push({
        name: `cargoedit`, // 只是把query改了，其他都没变
        query: {
          id: row["id"],
        },
      });
    },
    async addCargo(){
        this.cargoForm.user_id = JSON.parse(localStorage.getItem('user'))["id"]
        
        const response = await http
        .post("/cargos/add",
          {
            params: this.cargoForm,
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
      this.steps=1
    },
    resetForm() {
         Object.assign(this.cargoForm,{
            cargo_name:'',
            cargo_type:'',
            weight:''
        })
      },
  },
}
</script>

<style scoped>
.price{
    position: relative;
}
.payInfo{
    margin-top: 50px;
    /* position:absolute; */
    /* right:20px; */
    display: flex;
    justify-content: space-between;
}
.payInfo div:nth-child(2){
    margin-top: 50px;
}
.payValue{
    
    font-size: 40px;
    color: #CA3A1A 
;
}
.finish{
    
    position:absolute;
    right:5px;
}
.el-steps ,.form {
    display:flex;
    justify-content: center;
}
.el-steps{
   margin-left: 100px;

} 
.texterea{
    width: 400px; 
}
.h11 {
  display: flex;
  justify-content: space-between;
}
.cargo {
  width: 80%;
  margin: 0 auto;
}
.main {
  margin-top: 100px;
 
}

a{
    color:red
}

</style>