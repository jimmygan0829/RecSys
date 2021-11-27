<template>
  <div >
    
      <el-row type="flex" justify="center" align="middle">
        <el-form ref="loginForm" :model="user" status-icon label-width="80px">
          <h3 style="text-align: center;">Login</h3>
          <hr>
          <el-form-item prop="username" label="username">
            <el-input v-model="user.username" placeholder="Please input username" prefix-icon></el-input>
          </el-form-item>
          <el-form-item id="password" prop="password" label="password">
            <el-input v-model="user.password" show-password placeholder="Please input password"></el-input>
          </el-form-item>
          <router-link to="/register">Don't have a account? Click to register</router-link>
          <el-form-item style = "text-align: center;">
            <el-button type="primary" icon="el-icon-upload" @click="doLogin()">Login</el-button>
          </el-form-item>
        </el-form>
      </el-row>
    
  </div>
</template>
 
<script>
import axios from "axios";
export default {
  name: "login",
  data() {
    return {
      user: {
        username: "",
        password: ""
      }  
    };
  },
  created() {},
  methods: {
    doLogin() {
      if (!this.user.username) {
        this.$message.error("Please input username！");
        return;
      } else if (!this.user.password) {
        this.$message.error("Please input password！");
        return;
      } else {
        let data = {"username":this.user.username,"password":this.user.password}
        axios
          .post("/token/login/", data)
          .then(res => {
            
            if (res.status === 200) {
							let authToken = "Token " + res.data.auth_token
              this.$store.dispatch('setAuthToken', authToken);
              this.$store.dispatch('setUsername', this.user.username);
							console.log("Stored token:",this.$store.state.authToken)
              this.$router.push({path: "/" });
            } else {
              alert("Wrong username or password！");
            }
					})
					.catch(error => {
							if (error.response) {
								console.log(JSON.stringify(error.response.data))
								alert(JSON.stringify(error.response.data));
							}
							
      				
  				})
      }
    }
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login {
  width: 100%;
  height: 100%;
  background-color: cornsilk;
  background-size: cover;
  overflow: hidden;
  
}
.login-wrap {
  width: 400px;
  height: 300px;
  margin: 215px auto;
  overflow: hidden;
  padding-top: 10px;
  line-height: 40px;
}
#password {
  margin-bottom: 5px;
}
h3 {
  color: #0babeab8;
  font-size: 24px;
}
hr {
  background-color: #444;
  margin: 20px auto;
}
a {
  text-decoration: none;
  color: #aaa;
  font-size: 15px;
}
a:hover {
  color: coral;
}
.el-button {
  width: 80%;
  margin-left: -50px;
  margin-top: 20px;
}
.el-row{
  height:100%;
}
</style>
