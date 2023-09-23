<template>
  <div>
    <el-carousel :interval="4000" type="card" height="400px">
      <el-carousel-item v-for="item in imgList" :key="item">
        <h3 class="medium">
          <img :src="item.url" alt="" width="100%" height="100%">
        </h3>
      </el-carousel-item>
    </el-carousel>
    <div class="aboutUser">
      <div class="left">
        <h2>我的航运订单</h2>
        <div class="info">
          <div>
            <div class="icon">
            <img src="../../assets/welcome/order.svg" alt="" width="70px">
           </div>  
          <el-statistic title="总订单" :value="order_num">
            <!-- <template slot="formatter"> {{  }} </template> -->
          </el-statistic>
          </div>
          <div>
            <div class="icon">
            <img src="../../assets/welcome/daiorder.svg" alt="" width="70px">
           </div> 
          <el-statistic title="已完成订单" :value="order_ok_num">
            
          </el-statistic>
        </div>
          
        </div>

        <el-table :data="tableData" style="width: 85%">
          <el-table-column prop="orderNum" label="订单号"> </el-table-column>
          <el-table-column prop="cargo" label="货物"> </el-table-column>
          <el-table-column prop="end_port" label="目的地"> </el-table-column>
          <el-table-column prop="status" label="订单状态" width="100">
          </el-table-column>
        </el-table>
      </div>

      <div class="right">
        <h2>我的货物</h2>
        <div class="info">
          <div>
            <div class="icon">
            <img src="../../assets/welcome/cargo.svg" alt="" width="70px">
           </div> 
          <el-statistic group-separator="," :precision="0" decimal-separator="." :value="cargo_num" title="总货物">
            
          </el-statistic>
        </div>
        <div>
            <div class="icon">
            <img src="../../assets/welcome/cargo2.svg" alt="" width="70px">
           </div> 
          <el-statistic group-separator="," :precision="0" decimal-separator="." :value="cargo_ok_num" title="已完成货物">
            
          </el-statistic>
        </div>
         
        </div>
        <div
          class="echart"
          id="mychart"
          :style="{ float: 'left', width: '100%', height: '400px' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import http from "../../shared/Http.js";

export default {
  name: "MainBody",
  data() {
    return {
      cargo_num:0,
      cargo_ok_num:0,
      order_num:0,
      order_ok_num:0,
      userInfo:"",
      imgList:[
        {
            url:require('../../assets/zoumadeng/pic1.jpg') //url: '../assets/lake.jpg'      
        },
        {
            url:require('../../assets/zoumadeng/pic2.jpg') //url: '../assets/build.jpg' 
        },
        {
            url:require('../../assets/zoumadeng/pic3.jpg') //url: '../assets/road.jpg' 
        },
        {
            url:require('../../assets/zoumadeng/pic4.jpg') //url: '../assets/sea.jpg' 
        },
        {
            url:require('../../assets/zoumadeng/pic5.jpg') //url: '../assets/sea.jpg' 
        }
        ],

      tableData: [
      ],
      option: {}
    };
  },
  async beforeMount(){
    this.userInfo = JSON.parse(localStorage.getItem('user'))

    const response = await http
            .get("/getmain",
            {
              params: { user_id:this.userInfo['id'] },
            })
            .catch((error) => console.log(error));
            console.log(response.data);
            this.tableData = response.data["orders"]
            this.cargo_num = response.data["cargo_num"]
            this.cargo_ok_num = response.data["cargo_ok_num"]
            this.order_num = response.data["ord_num"]
            this.order_ok_num = response.data["ord_ok_num"]
            this.option = {
                title: {
                  text: "我的货物分类",
                  left: "center",
                  top: "center",
                },
                series: [
                  {
                    type: "pie",
                    data: response.data["seriesData"],
                    radius: ["40%", "70%"],
                  },
                ],
             }
             this.initEcharts();
  },
  
  methods:{
    initEcharts() {
      
      const myChart = echarts.init(document.getElementById("mychart"));// 图标初始化
      myChart.setOption(this.option);// 渲染页面
      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    }
  }
};
</script>

<style scoped>
.info div{
    display: flex;
   justify-content: space-between;
    background: #f0f2f5;
    border-radius: 16px;
}
.info div:nth-child(1){
  margin-right: 10px;
}
.icon {
  padding-left: 50px;
}
.el-statistic{
   
   flex-direction: column;
   width: 40%;
   
   font-weight: 700;
   margin: 26px;
   margin-left: 0;
}
.el-table{
  margin-top: 20px;
}
.aboutUser .info {
  display: flex;
}
.aboutUser .info div {
  flex: 1;
  
}
h3 {
  text-align: center;
}
.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}
h2 {
  margin-bottom: 20px;
}
.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
.el-carousel {
  margin-bottom: 80px;
}
.aboutUser {
  height: 100%;
  padding: 50px;
  display: flex;
}
.aboutUser div {
  flex: 1;
}

.left {
  /* border-right: 1px solid #000; */
}
.el-table {
  margin-left: 25px;
}
/deep/.el-table thead tr > th {
  background-color: #8bd3e1;
}
/deep/.el-table tbody tr > td {
  background-color: #ddeef1;
}
.sum_order {
  border: 5px solid #bd891a;
  border-radius: 50%;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
  font-size: 50px;
}
.sum_cargo {
  border: 5px solid #bd891a;
  border-radius: 50%;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
  font-size: 50px;
}
.sum_not_order {
  border: 5px solid #29e94c;
  border-radius: 50%;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
  font-size: 50px;
}
.el-divider {
  width: 1px;
}
</style>