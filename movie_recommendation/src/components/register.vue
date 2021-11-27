<template>
  <div>
    
      <el-row type="flex" justify="center" align="middle">
        <el-form ref="loginForm" :model="user" status-icon label-width="80px">
          <h3 style="text-align: center;">Register</h3>
          <hr>

          <el-form-item prop="username" label="username">
            <el-input v-model="user.username" placeholder="Please input username"></el-input>
          </el-form-item>
          
          <el-form-item prop="firstname" label="firstname">
            <el-input v-model="user.firstname" placeholder="Please input firstname"></el-input>
          </el-form-item>

          <el-form-item prop="lastname" label="lastname">
            <el-input v-model="user.lastname" placeholder="Please input lastname"></el-input>
          </el-form-item>

          
          <el-form-item prop="email" label="email">
            <el-input v-model="user.email" placeholder="Please input email"></el-input>
          </el-form-item>
          <el-form-item prop="password" label="password">
            <el-input v-model="user.password" show-password placeholder="Please input password"></el-input>
          </el-form-item>
          <el-form-item prop="re_password" label="password*">
            <el-input v-model="user.re_password" show-password placeholder="Input password again"></el-input>
          </el-form-item>
          <div>
            <el-button type="primary" icon @click="doRegister()">Register</el-button>
          </div>
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
        email: "",
        password: "",
        firstname: "",
        lastname:"",
        re_password:""
      },
    };
  },
  created() {

  },
  methods: {
    doRegister() {
			if (!this.user.firstname) {
        this.$message.error("Please input firstname！");
        return;
			} else if (!this.user.lastname) {
        this.$message.error("Please input lastname");
        return;
      } else if (!this.user.username) {
        this.$message.error("Please input username！");
        return;
      } else if (!this.user.email) {
        this.$message.error("Please input email！");
        return;
      } else if (this.user.email != null) {
        var reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
        if (!reg.test(this.user.email)) {
          this.$message.error("Please input valid email！");
        } else if (!this.user.password) {
          	this.$message.error("Please input password！");
          return;
        } else if (!this.user.re_password) {
          	this.$message.error("Please input password again！");
          return;
        }else {
					let data = {
						"username":this.user.username,
						"first_name":this.user.firstname,
						"last_name":this.user.lastname,
						"email":this.user.email,
						"password":this.user.password,
						"re_password":this.user.re_password
					}
          axios
            .post("/users/", data)
            .then(res => {
              console.log(res)
              if (res.status === 201 && res.data) {
								alert("Register successfully")
								this.$router.push({path: "/login" });
              } else {
								alert(res)
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
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

 
h3 {
  color: #0babeab8;
  font-size: 24px;
}
hr {
  background-color: #444;
  margin: 20px auto;
}
 
.el-button {
  width: 80%;
  margin: 0 auto;
  display: block;
}
</style>