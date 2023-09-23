<template>
    <div style="width: 80%;margin: 0 auto;">
        <div class="h11">
            <h1><i class="el-icon-s-goods"></i>订单号：{{ id }}</h1></div>
           <div class="main">
            <el-form
                    label-position="right"
                    label-width="80px"
                    
                    size="medium"
                >
          <el-form-item label="船只">
              {{ data.ship }}
          </el-form-item>
          <el-form-item label="货物">
            {{ data.cargo }}
           
          </el-form-item>

          <el-form-item label="起始港口">
            {{ data.start_port }}
          </el-form-item>
          <el-form-item label="目的港口">
            {{ data.end_port }}
           
          </el-form-item>
            <el-form-item label="订单备注">
                {{ data.Remark }}
                
            </el-form-item>
            <el-form-item label="订单状态">
                {{ data.status }}
                
            </el-form-item>
            <el-form-item label="订单金额">
                {{ data.price }}
                
            </el-form-item>
            <el-form-item v-if="data.kuaidiNum!== ''" label="快递单号">
              {{ data.kuaidiNum}}
              
           </el-form-item>
                </el-form>
                <div class="right">
                  <div v-if="getOrderStatus==='待支付'" class="payInfo" >
                            <div>
                                <img src="../../assets/支付二维码.png" alt="" width="100px">
                            </div>
                            <div >
                                需要支付：<span class="payValue">¥{{ this.data["price"] }}</span>
                            </div>
                            <div class="finish">
                            <el-button type="success" round @click="finishPay">支付完成</el-button>
                        </div>
                        </div>
                  <div v-else-if="getOrderStatus==='待收货'">
                  
                    <div class="cirle-move">
                        <img class="avtar"
                            src="../../assets/order/shipMove.svg" />
                    </div>


                    <h1>正在运输😊 请耐心等候</h1>
                    <h2>这是你的快递单号：{{ data.kuaidiNum }}</h2>
                    <el-button type="primary" round @click="finishYunshu" style="margin-left: 50px;margin-top: 20px;">确认收货</el-button>
                    

                </div>
                <div v-else-if="getOrderStatus==='待评价'">
                  <h1 style="margin-bottom: 50px;">请评价</h1>
                  <el-rate style="margin-bottom: 20px;"
                      v-model="comment"
                      :colors="colors">
                  </el-rate>
                  <el-button type="primary" round @click="subComment">提交评价</el-button>
                </div>
                <div v-else-if="getOrderStatus==='待发货'">
                  <img  src="../../assets/order/package.svg" />
                   <h1>请耐心等待发货</h1>
                </div>
                <div v-else-if="getOrderStatus==='已完成'">
                  <el-result icon="success" title="完成订单" subTitle="消费愉快">
                    <template slot="extra">
                    <router-link to="/main/order">
                      <el-button type="primary" size="medium">返回</el-button>
                    </router-link>
                    
                  </template>
                </el-result>
                </div>
                <div v-else-if="getOrderStatus==='已取消'">
                 
                <el-result icon="error" title="错误提示" subTitle="请根据提示进行操作">
                  <template slot="extra">
                    <router-link to="/main/order">
                      <el-button type="primary" size="medium">返回</el-button>
                    </router-link>
                    
                  </template>
                </el-result>
                </div>
                </div>
                
           </div>
        
    </div>
</template>

<script>
import http from "../../shared/Http.js";

export default {
    name:"OrderAllInfo",
    data(){
        return{
            id:"",
            data:{},
            comment: null,
            colors: ['#99A9BF', '#F7BA2A', '#FF9900']
        }
    },
    computed:{
      getOrderStatus(){
        return this.data.status
      }
    },  
    async beforeMount(){
         this.id = this.$route.query.id
         const response = await http.get('/getOrderById',{
              params: {"id":this.id}},{        
                headers: {  //头部参数
                'Content-Type': 'application/json',
                }
            }
          ).catch(error =>console.log(error))
         this.data = response.data["orders"][0]
    },
    methods: {
    async finishPay(){
        const response = await http
        .post(
          "/orders/pay",
          {
            params: { orderNum: this.id },
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
       
        window.location.reload();
    },
    async finishYunshu(){
        const response = await http
        .post(
          "/orders/qianshou",
          {
            params: { orderNum: this.id },
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
        window.location.reload();
    },
    async subComment(){
      const response = await http
        .post(
          "/orders/comment",
          {
            params: { orderNum: this.id ,comment:this.comment },
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
        window.location.reload();
    }
  }
}
</script>

<style scoped>
.cirle-move{
  animation: forward 4s;
}
    .avtar {
        width: 7.5rem;
        height: 7.5rem;
       
        position: relative;
      animation: forward 4s infinite;
    }

   
    @keyframes forward {
        0% {
          left: 0;
          
        }
        50% {
          left: 200px;
        }
        100% {
          left: 400px;
        }
    }

     
    




.main{
  background: #fff;
  border-radius: 20px;
  display: flex;
  justify-content: space-between;
}
.right{
  /* top: 200px;
  right: 100px;
  position:relative; */
  flex: 1;
  display: flex; /**/
            justify-content: center; /*水平居中*/
            align-items: Center; /*垂直居中*/
  
}
.payValue{
    
    font-size: 40px;
    color: #CA3A1A 
;
}
</style>