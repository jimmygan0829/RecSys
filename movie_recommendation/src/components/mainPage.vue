<template>
  <div>
    
    <el-menu
			class="el-menu-demo"
			mode="horizontal"
			@select="handleSelect"
			background-color="#545c64"
			text-color="#fff"
			active-text-color="#ffd04b"
			>
			
			<el-menu-item index="Home">Home</el-menu-item>
			<el-menu-item  style = "float: right" v-show="$store.state.authToken == ''" index="login">Login</el-menu-item>
			<el-menu-item  style = "float: right" v-show="$store.state.authToken != ''" index="logout">Logout</el-menu-item>
			<el-menu-item  style = "float: right" v-show="$store.state.authToken != ''" index="username">{{$store.state.username}}</el-menu-item>
			<el-menu-item style = "float: right" v-show="$store.state.authToken == ''" index="register">Register</el-menu-item>
    </el-menu>

		<div style = "  margin-left: 1%;width: 100%;overflow:auto;" v-for="(eachMovieCatogory,name) in mainPageResponse" :key="name">
			<h2>{{name}}</h2>
			<div style="display:inline-flex">
				<div style="margin-right:1vw;" v-for="(eachMovie,id) in eachMovieCatogory.recommendation" :key="id">
					<img style="width:20vw;height:15vw;border-radius:15px;" :src="eachMovie.img_link" alt="" @click="goToNextMovieIntro(id)">
				</div>
			</div>

			
		</div>
		
    

  </div>
</template>
 
<script>
import axios from "axios";
import { MessageBox } from 'element-ui';
export default {
  name: "mainPage",
  data() {
    return {
			mainPageResponse:''
    };
  },
  created() {
		this.fetchMovie();
  },
  methods: {
    handleSelect(key, keyPath) {
        if (key == "Home") {
					this.$router.push({path: "/" });
				} else if(key == "login"){
					this.$router.push({path: "/login" });
				} else if(key == "logout"){
					this.clearToken();
				} else if(key == "register"){
					this.$router.push({path: "/register" });
				}
    },
		clearToken(){
			this.$store.state.authToken = ''
			this.$store.state.username = ''
			console.log("Clear token and username")
		},
		goToNextMovieIntro(id){
			// Verify if auth token exists
			if(this.$store.state.authToken == ''){
				this.$confirm('Login is required to view movie introduction, Would you like to login your account?', 'Hint', {
          confirmButtonText: 'login',
          cancelButtonText: 'cancel',
          type: 'hint'
        }).then(() => {
          this.$router.push({
        		path:'/login'
      		})
        }).catch(() => {
                   
        });
			} else{
				this.$router.push({
        	path:'/movieIntro/' + id
      	})
			}

		},
		fetchMovie(){
			let that = this;
			if (this.$store.state.authToken == '') {
					axios.get('/api/landing/home',{
					
					})
					.then(function (response) {
						// handle success
						that.mainPageResponse = response.data
						
						console.log("MainPage api: ", that.mainPageResponse);
					})
					.catch(function (error) {
						// handle error
						console.log(error);
					})
				}
			else {
				axios.get('/api/landing/home',{
					headers:{
						'Authorization':that.$store.state.authToken,
					}
				})
				.then(function (response) {
					// handle success
					that.mainPageResponse = response.data
					
					console.log("MainPage api: ", that.mainPageResponse);
				})
				.catch(function (error) {
					// handle error
					console.log(error);
				})
			}
		} 
		
    
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

 
</style>