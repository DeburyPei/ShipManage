<template>
    <el-container>
        <el-header>
            <Header />
        </el-header>
        <el-main>
           <router-view ></router-view>
        </el-main>
    </el-container>
</template>

<script>
import Header from "../components/main/header.vue"

export default {
        name:"Main",
        components:{
            Header
        }
}
</script>

<style scoped>
.el-header{
    padding: 0;
}
.el-main{
    background: #F1F6F7;
    height:95vh;
}
</style>