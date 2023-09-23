<template>
  <div class="order">
    <div class="h11">
      <h1><i class="el-icon-s-goods"></i>我的订单</h1>
      <el-button type="success" round @click="isReadOrWrite = !isReadOrWrite">{{
        buttonText
      }}</el-button>
    </div>
    <div class="main">
      <div class="options" v-if="isReadOrWrite">
        <el-table
            :data="tableData"
            border
            style="width: 100%">
           
            <el-table-column
            prop="orderNum"
            label="订单编号"
            width="100">
            </el-table-column>
            <el-table-column
            prop="cargo"
            label="货名"
           >
            </el-table-column>
            <el-table-column
            prop="ship"
            label="船舶"
           
            >
            
            </el-table-column>
            <el-table-column
            prop="start_port"
            label="起始港口"
            
            >
            </el-table-column>
            
            <el-table-column
            prop="end_port"
            label="目的港口"
            
            ></el-table-column>
            <el-table-column
            prop="price"
            label="价格"
            
            ></el-table-column>
            
           
            <el-table-column
            prop="status"
            label="订单状态"
            width="100"
            >
            
            </el-table-column>
            
            <el-table-column label="操作" width="200">
                <template slot-scope="scope">
                    <el-button
                    size="mini"
                    @click="handleEdit(scope.$index, scope.row)">订单详情</el-button>
                    <el-button
                    size="mini"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)">取消订单</el-button>
                </template>
            </el-table-column>
        </el-table>
    
    </div>
      <div class="options" v-else>
        <el-steps :space="200" :active="steps" finish-status="success">
            <el-step title="创建订单"></el-step>
            <el-step title="付款订单"></el-step>
            <el-step title="完成订单"></el-step>
        </el-steps>
        <div class="form">
            <div v-if="steps===0">
                <el-form
                    label-position="right"
                    label-width="80px"
                    :model="formLabelAlign"
                    size="medium"
                >
          <el-form-item label="选择船只">
            <el-select v-model="shipValue" placeholder="请选择">
                <el-option
                    v-for="item in shipOptions"
                    :key="item.name"
                    :label="item.name"
                    :value="item.id">
                </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="选择货物">
            <el-select v-model="cargoValue" placeholder="请选择">
                <el-option
                v-for="item in cargoOptions"
                :key="item.name"
                :label="item.name"
                :value="item.id">
                </el-option>
            </el-select>
            <router-link to="/main/cargo">
                <span>没有货物请添加货物</span> 

            </router-link>
          </el-form-item>
          
          <el-form-item label="起始港口">
            <el-select v-model="startPort" placeholder="请选择">
                <el-option
                v-for="item in portOptions"
                :key="item.name"
                :label="item.name"
                :value="item.id">
                </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="目的港口">
            <el-select v-model="endPort" placeholder="请选择">
                <el-option
                v-for="item in portOptions"
                :key="item.name"
                :label="item.name"
                :value="item.id">
                </el-option>
            </el-select>
          </el-form-item>
            <el-form-item label="订单备注">
                <el-input type="textarea" class="texterea" v-model="reMark"
                :autosize="{ minRows: 5, maxRows: 10}"
                ></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">立即创建</el-button>
                <el-button @click="isReadOrWrite=true">取消</el-button>
            </el-form-item>
                </el-form>
            </div>
            <div v-else-if="steps===1">
                <h3 style="margin-top:40px;margin-right: 40px;text-align: center;margin-bottom: 20px;">订单金额细节</h3>
                <div class="price">
                        <el-table
                            :data="showSubForm"
                            style="width: 100%">
                            <el-table-column
                                prop="orderNum"
                                label="订单号"
                               >
                            </el-table-column>
                            <el-table-column
                                prop="ship_Name"
                                label="船名"
                                width="70">
                            </el-table-column>
                           
                            
                        
                            <el-table-column
                                prop="cargo_Name"
                                label="货物名"
                               >
                            </el-table-column>
                            <el-table-column
                                prop="startPort_Name"
                                label="起始港">
                            </el-table-column>
                            <el-table-column
                                prop="endPort_Name"
                                label="目的港">
                            </el-table-column>
                            <el-table-column
                                prop="distance"
                                label="路程 KM">
                            </el-table-column>
                        </el-table>
                        <div class="payInfo">
                            <div>
                              <el-statistic :value="deadline2" time-indices title="付款倒计时">
                                
                              </el-statistic>
                                <img src="../../assets/支付二维码.png" alt="" width="100px">
                            </div>
                            <div >
                                需要支付：<span class="payValue">¥{{ showSubForm[0]?.price }}</span>
                            </div>
                        </div>
                        <div class="finish">
                            <el-button type="success" round @click="finishPay">支付完成</el-button>
                        </div>


                        
                </div>
            </div>
            <div v-else-if="steps===2">
                <el-result icon="success" title="完成订单" subTitle="请根据提示进行操作">
                    <template slot="extra">
                        <el-button type="primary" size="medium" @click="refresh">查看订单</el-button>
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
function setTimeDateFmt(s) {  // 个位数补齐十位数
    return s < 10 ? '0' + s : s;
}

function createordernum() {
    const now = new Date()
    let month = now.getMonth() + 1
    let day = now.getDate()
    let hour = now.getHours()
    let minutes = now.getMinutes()
    let seconds = now.getSeconds()
    month = setTimeDateFmt(month)
    day = setTimeDateFmt(day)
    hour = setTimeDateFmt(hour)
    minutes = setTimeDateFmt(minutes)
    seconds = setTimeDateFmt(seconds)
    let orderCode = now.getFullYear().toString() + month.toString() + day + hour + minutes + seconds + (Math.round(Math.random() * 1000000)).toString();
    return orderCode;
    //基于年月日时分秒+随机数生成订单编号
}


export default {
  name: "MyOrder",
  data() {
    return {
      deadline2: Date.now() + 1000 * 60 * 15 ,
        orderNum:"",
        userInfo:{},
      steps:0,
      isReadOrWrite: true,
      formLabelAlign: {
        name: "",
        region: "",
        type: "",
      },
      shipOptions:[],
      shipValue: "",
      cargoOptions:[],
      cargoValue: "",
      portOptions:[],
      startPort:"",
      endPort:"",
      reMark:"",
      subForm:{},
      showSubForm:[],
      tableData:[]
    };
  },
  async beforeMount() {
    this.userInfo = JSON.parse(localStorage.getItem('user'))
    
    const response = await http
            .get("/createOrderInfo",
            {
              params: { user_id:this.userInfo['id'] },
            })
            .catch((error) => console.log(error));
            this.shipOptions = response.data["ships"]
            this.cargoOptions = response.data["cargos"]
            this.portOptions = response.data["port"]
            const orderResponse = await http
            .get("/getOrder",
            {
              params: { id:this.userInfo['id'] },
            }).catch((error) => console.log(error));
            this.tableData = orderResponse.data["orders"]
  },
  computed: {
    buttonText() {
      return this.isReadOrWrite ? "立刻下单" : "查看订单";
    },
    
  },
  methods:{
    refresh() {
      window.location.reload();
    },
    getId_to_Name(id,name){
        let options = []
        if(name==="ship"){
            options= this.shipOptions
        }else if(name==="cargo"){
            options= this.cargoOptions
        }else{
            options = this.portOptions
        }
        for(let i of options){
            console.log(i)
            if(i["id"]===id){
                return i["name"]
            }
        }
        return 

    },
    
    async onSubmit(){
        this.orderNum = createordernum()
        this.subForm = {
            orderNum:this.orderNum,
            shipId : this.shipValue,
            cargoId : this.cargoValue,
            startPortId: this.startPort,
            endPortId: this.endPort,
            reMark:this.reMark,
            
            
            user_id:this.userInfo['id']
        }
       
       
        const response = await http
            .post("/createOrder",
            {
              params: this.subForm,
            })
            .catch((error) => {console.log(error);this.$message.error("错了哦，这是一条错误消息");});
            if (response.status === 200) {
              this.$message({
              message: "恭喜你，这是一条成功消息",
              type: "success",
              });

            this.steps = 1
            this.showSubForm.push(
              {   
                  ship_Name:this.getId_to_Name(this.subForm["shipId"],"ship"),
                  cargo_Name:this.getId_to_Name(this.subForm["cargoId"],"cargo"),
                  startPort_Name:this.getId_to_Name(this.subForm["startPortId"],"port"),
                  endPort_Name:this.getId_to_Name(this.subForm["endPortId"],"port"),
                  price:response.data["price"],
                  distance:response.data["distance"],
                  orderNum:this.orderNum,
              }
            )
        }
      console.log(this.showSubForm)
      console.log(response.data)
    },
    async finishPay(){
        const response = await http
        .post(
          "/orders/pay",
          {
            params: { orderNum: this.orderNum },
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
        this.steps = 2
       
    },
    handleEdit(index, row) {
      this.$router.push({
        name: `orderAllInfo`, // 只是把query改了，其他都没变
        query: {
          id: row["orderNum"],
        },
      });
    },
    async handleDelete(index, row){
      
      if(["待发货","待支付"].indexOf(row["status"]) !== -1){
        const response = await http
        .post(
          "/orders/quxiao",
          {
            params: { orderNum: row['orderNum'] },
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
      } 
      }else{
        this.$message.error("对不起 只有在发货之前才可以取消订单");

      }
     
    }
  }
};
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
.order {
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