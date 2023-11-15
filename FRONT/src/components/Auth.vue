<template>

  <!-- <div class="is-loading-bar has-text-centered"  style="text-align:center;" v-bind:class="{'is-loading': this.$store.state.isLoading }">
    <div class="lds-dual-ring"></div>
  </div> -->
  <!-- <br> -->
  
  <div class="login-form">
    <div class="text">
      LOGIN
    </div>
    <vee-form :validation-schema="loginSchema" @submit="loginAuth" class="veeform">
      <div class="field">
          <v-icon color="info" icon="mdi-mail" class="fas"></v-icon>
          <vee-field type="email" name="email" class="veeinput" placeholder="Email" />
      </div>
      <ErrorMessage style="color:red;" name="email" />  
      <div class="field">
          <v-icon color="info" icon="mdi-lock" class="fas"></v-icon>
          <vee-field type="password" name="password" autocomplete="on" class="veeinput" placeholder="Password" />
      </div>
      <ErrorMessage style="color:red;" name="password" />
      <button class="submit" type="submit" :disabled="login_in_submission">
        LOGIN
      </button>
      <!-- <div class="link">
          Not a member?
          <a href="#">Signup now</a>
      </div> -->
    </vee-form>
    <br>
    <div v-if="login_show_alert" :style="login_alert_variant" style="text-align:center;">
      {{ login_alert_msg }}
    </div>
  </div>
</template>

<script>
import { useCounterStore } from '@/stores/counter';
import { mapState } from 'pinia'
import { mapWritableState } from 'pinia'
import { mapActions } from 'pinia'

export default {
  name: 'LoginForm',
  data() {
    return {
      loginSchema: {
        email: 'required|email',
        password: 'required|min:3|max:32',
      },
      login_in_submission: false,
      login_show_alert: false,
      login_alert_variant: 'color: #c7c7c7;  border: 1px solid #1a1a1a; box-shadow:0 0 5px rgba(52, 152, 219, .3), 0 0 10px rgba(52, 152, 219, .2), 0 0 15px rgba(52, 152, 219, .1), 0 1px 0 black',
      login_alert_msg: 'Please wait! We are logging you in.',
    };
  },
  methods: {
    
    ...mapActions(useCounterStore, ['login']),

    async loginAuth(values) {
      this.isLoading = true;

      this.login_in_submission = true;
      this.login_show_alert = true;
      this.login_alert_variant = 'color: white; background-color:#1a1a1a;  border: 1px solid #1a1a1a; box-shadow:0 0 5px rgba(52, 152, 219, .3), 0 0 10px rgba(52, 152, 219, .2), 0 0 15px rgba(52, 152, 219, .1), 0 1px 0 #1a1a1a4';
      this.login_alert_msg = 'Please wait! We are logging you in.';

      try {
        console.log(values)
        await this.login(values);

        this.isLoading = false;
      } catch (error) {
        this.isLoading = false;

        this.login_in_submission = false;
        this.login_alert_variant = 'color: white; background-color:#990000;  border: 1px solid #990000;  box-shadow: 0 0 5px rgba(255,0,0,.3), 0 0 10px rgba(255,0,0,.2), 0 0 15px rgba(255,0,0,.1), 0 1px 0 #990000';
        this.login_alert_msg = 'Invalid login details';
        return;
      }

      this.login_alert_variant = 'color: white; background-color:#339933; border: 1px solid #339933; box-shadow: 0 0 5px rgba(0,255,0,.3), 0 0 10px rgba(0,255,0,.2), 0 0 15px rgba(0,255,0,.1), 0 1px 0 #339933;';
      this.login_alert_msg = 'Success! You are now logged in.';
      
      this.$router.push('/').then(() => {
        window.location.reload();
      });
    },
  },
  computed:{
    ...mapWritableState(useCounterStore, ['isLoading']),
  //  ...mapState(useCounterStore, ['isLoading'])

  }
};
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Poppins&display=swap');

.login-form{
  position: relative;
  width: 370px;
  height: auto;
  // background: #1b1b1b;
  background-image: linear-gradient(to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)), url('../src/assets/images/background3.jpg'); 
  background-size: cover;
  padding: 40px 35px 60px;
  box-sizing: border-box;
  border: 1px solid black;
  border-radius: 5px;
  box-shadow: inset 0 0 1px #272727;
}
.text{
  font-size: 30px;
  color: white;
  font-weight: 600;
  letter-spacing: 2px;
  // text-align:center;
}
.veeform{
  margin-top: 40px;
}
.veeform .field{
  margin-top: 20px;
  display: flex;
}
.field .fas{
  height: 50px;
  width: 60px;
  color: #868686;
  font-size: 20px;
  line-height: 50px;
  border: 1px solid #444;
  border-right: none;
  border-radius: 5px 0 0 5px;
  background: linear-gradient(#333,#222);
}
.field .veeinput,.veeform button{
  height: 50px;
  width: 100%;
  outline: none;
  font-size: 19px;
  color: #868686;
  padding: 0 15px;
  border-radius: 0 5px 5px 0;
  border: 1px solid #444;
  caret-color: #3399cc;
  background: linear-gradient(#333,#222);
}
.veeinput:focus {
  color: #3399cc;
  box-shadow: 0 0 5px rgba(0, 191, 255, 0.2),
              inset 0 0 5px rgba(0, 191, 255, 0.1);
  background: linear-gradient(#333933, #222922);
  animation: glow .8s ease-out infinite alternate;
}

@keyframes glow {
  0% {
    border-color: #3399cc;
    box-shadow: 0 0 5px rgba(0, 191, 255, 0.2),
                inset 0 0 5px rgba(0, 0, 0, 0.1);
  }
  100% {
    border-color: #99ccff;
    box-shadow: 0 0 20px rgba(0, 191, 255, 0.6),
                inset 0 0 10px rgba(0, 191, 255, 0.4);
  }
}

.submit{
  margin-top: 30px;
  border-radius: 5px!important;
  font-weight: 600;
  letter-spacing: 1px;
  cursor: pointer;
}
.submit:hover{
  color: #3399cc;
  border: 1px solid #3399cc;
  box-shadow: 0 0 5px rgba(0, 191, 255, 0.3),
              0 0 10px rgba(0, 191, 255, 0.2),
              0 0 15px rgba(0, 191, 255, 0.1),
              0 1px 0 black;
}
.link{
  margin-top: 25px;
  color: #868686;
}
.link a{
  color: #339933;
  text-decoration: none;
}
.link a:hover{
  text-decoration: underline;
}

</style>