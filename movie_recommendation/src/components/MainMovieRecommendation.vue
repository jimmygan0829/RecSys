<template>
  <div class="mainMovieRecommendation">
    <el-menu
			class="el-menu-demo"
			mode="horizontal"
			@select="handleSelect"
			background-color="#545c64"
			text-color="#fff"
			active-text-color="#ffd04b"
			>
			
			<el-menu-item index="Home">Home</el-menu-item>
			<el-menu-item  style = "float: right" v-show="$store.state.authToken != ''" index="username">{{$store.state.username}}</el-menu-item>
			
    </el-menu>

    <div class="mainMovieRecommendation-mainMovie">
      <img class = "mainMovieRecommendation-mainMoviePic" :src="'https://filmimg.s3.us-west-2.amazonaws.com/' + mainMovieId + '.jpg'" alt="">
      <div class="mainMovieRecommendation-mainMovieInfo">
        <div class="mainMovieRecommendation-mainMovieTitle">{{mainMovieTitle}}</div>
        <div class="mainMovieRecommendation-mainMovieCatagory">{{mainMovieGenres+" · "+mainMovieRuntime}}</div>
        <div class="mainMovieRecommendation-mainMovieRating">
          <el-rate
            v-model="value"
            disabled
            show-score
            text-color="black"
            :score-template="'Global score: ' + mainMovieRating">
          </el-rate>
        </div>
        <div class="mainMovieRecommendation-mainMovieRating">
          <el-rate
            v-model="mainMovieUserRating"
            @change="changeRate"
            show-score
            allow-half
            text-color="black"
            :score-template="'User score: ' + mainMovieUserRating">
          </el-rate>
        </div>
        <p style="font-size:1.5rem;font-weight:800">Overview</p>
        <p>{{mainMovieStoryLine}}</p>
        
      </div>
    </div>
    <h2 style="margin-left:2%">Recommendations</h2>
    <div class="mainMovieRecommendation-recommendedMovie">     
      <div class="mainMovieRecommendation-recommendedMovieInfo">
        <div style="width:20vw;margin-right:1vw;" v-for="(recommendationMovie,i) in recommendationList" :key=i>
          <img style="width:20vw;height:15vw;border-radius:15px" :src=recommendationMovie.img_link alt="" @click="goToNextMovieIntro(i)">
            <div style="display:flex;justify-content:flex-end">
              <div style="margin-right:auto">{{recommendationMovie.title}}</div>
              <div >{{recommendationMovie.avg_rate + "%"}}</div>
            </div>
        </div>  
      </div>       
    </div>

    <h2 style="margin-left:2%">Comments</h2>
    <div style="margin-left:2%;margin-right:2%;display:flex;margin-bottom:2%">
      <el-input
        type="textarea"
        :autosize="{ minRows: 2, maxRows: 4}"
        placeholder="Please input your comments"
        :clearable="true"
        v-model="textarea2">
      </el-input>
      <el-button style="margin-left:1%" type="primary" icon @click="postComment()">Post comment</el-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  
  data () {
    return {
      value:0,
      // Main movie display
      mainMovieId:this.$route.params.id,
      mainMovieTitle:'',
      mainMovieGenres:'',
      mainMovieRuntime:'',
      mainMovieRating:'',
      mainMovieStoryLine:'',
      mainMovieYear:'',
      // Movie recommendation related to the main movie
      recommendationList:{
        
      },
      mainMovieUserRating:0,
      textarea2:"",
    }
  },
  created () {
    this.fetchMovieData(this.mainMovieId)
      
  },
  methods:{
    goToNextMovieIntro(id){
      this.$router.push({
        path:'/movieIntro/' + id
      })
    },
    fetchMovieData(movieId){
      let that = this;
      axios.get('/api/movie/detail',{
        params:{
          id:movieId
        },
        headers:{
          'Authorization':that.$store.state.authToken,
        }
      })
        .then(function (response) {
          // handle success
          console.log("Main movie's information: ", response);
          that.mainMovieGenres = response.data.main.genres;
          that.mainMovieRuntime = response.data.main.runtime;
          that.mainMovieStoryLine = response.data.main.storyline;
          that.mainMovieTitle = response.data.main.title;
          that.mainMovieYear = response.data.main.year;
          that.mainMovieRating = response.data.main.score;
          that.recommendationList = response.data.recommendation;
          if (response.data.main.user_score == 'None') {
            that.mainMovieUserRating = 0
          } else{
            that.mainMovieUserRating = response.data.main.user_score;
          }          
          if (isNaN(that.mainMovieRating)) {
            that.value = that.mainMovieRating / 100 * 5;
          } else{
            that.value = Number(that.mainMovieRating) / 100 * 5;
            
          }
        
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        })
        

    },
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
    changeRate(score){
      let that = this
      
      axios.post('/api/score/scupdate/',
        {"movieid":this.mainMovieId,"rating":score},
        {
          headers:{'Authorization':that.$store.state.authToken},
        }
      )
        .then(function (response) {
          console.log("User rating response: ", response)
          // handle success
          if (response.status == "200" && response.data.status == "valid") {
            that.$message.info("You have rated \"" + that.mainMovieTitle + "\" Score: " + score)
          }
          
        
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        })
      
    },
    postComment(){
      
      let that = this
      axios.post('/api/comment/pushcom/',
        {"movieid":this.mainMovieId,"comment":this.textarea2},
        {
          headers:{'Authorization':that.$store.state.authToken},
        }
      )
        .then(function (response) {
          console.log("Comment response: ",response)
          // handle success
          if (response.status == "200" && response.data.status == "valid") {
            that.$message.info("You have commented \"" + that.mainMovieTitle + "\"")
          }
          
        
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        })
    }
  },


  
  beforeRouteUpdate(to,from,next) {
    // 对路由变化作出响应
    console.log("To的id",to.params.id)
    console.log("from的id",from.params.id)
    if(to.params.id != from.params.id){      
      new Promise((resolve,reject) => {
        this.fetchMovieData(to.params.id);
        resolve();
      }).then(() => {
        this.mainMovieId = to.params.id
        next();
      })
      
      
    }
  }
  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.mainMovieRecommendation{
  font-family: 'Times New Roman', Times, serif;
}
.mainMovieRecommendation-mainMovie{
  display:flex;
  background:#E1DEDD;
  padding-top: 2%;
  padding-bottom: 5%;
}
.mainMovieRecommendation-mainMoviePic{
  margin-left: 4%;
  margin-right: 2%;
  width: 20vw;
  height: 29.82vw;
  border-radius: 15px;
}
.mainMovieRecommendation-mainMovieInfo{
  margin-right: 4%;
  
}
.mainMovieRecommendation-mainMovieTitle{
  font-size: 2rem;
  font-weight: 800;
}
.mainMovieRecommendation-mainMovieCatagory{
  margin-top: 0.5rem;
  color:#343434
}
.mainMovieRecommendation-mainMovieRating{
  margin-top: 1rem;
  font-size: 1rem;
  font-weight: 700;
}
.mainMovieRecommendation-recommendedMovie{
  margin-left: 2%;
  width: 92%;
  overflow:auto;
}
.mainMovieRecommendation-recommendedMovieInfo{
  display: inline-flex;
}
</style>
