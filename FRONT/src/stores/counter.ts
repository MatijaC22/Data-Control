import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import axios from 'axios'
import qs from 'qs';


interface LoginValues {
  email: string;
  password: string;
}
interface UserDelete {
  id: number
}
interface User {
  id?: number;
  name: string;
  surname: string;
  password: string;
  email: string;
  date_of_birth?: Date;
  image_url?: string;
  nationality: string;
  access_level: number;
  active: boolean;
}

export const useCounterStore = defineStore({
  id: 'auth',
  state: () => ({
    isLoading: false,

    searchQuery: null,

    userLoggedIn: false,
    setAuthToken:null,
    setAuthTokenType:null,
    setUserId:null,
    setUsername:null,
    tab:null,
    BASE_URL: 'http://localhost:8000/',
    // BASE_URL: 'https://d7b2-219-92-69-253.ngrok-free.app/api/',
    userData:null,
  }),
  getters: {
    // setIsLoading: (state:any, status:any) => {
    //   return state.isLoading = status
    // },
    // doubleCount: (state) => state.counter * 2
  },
  actions: {
    async login(values:LoginValues) {

      const data = qs.stringify({
        grant_type: '',
        username: values.email,
        password: values.password,
        scope: '',
        client_id: '',
        client_secret: ''
      });
      
      await axios.post(this.BASE_URL + 'login', data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }
      })
        .then(response => {
          console.log('Data was successfully submitted.', response);
          // this.setAuthToken = (<any>response).data.access_token
          // this.setAuthTokenType = (<any>response).data.token_type
          // this.setUserId = (<any>response).data.user_id
          // this.setUsername = (<any>response).data.username
          localStorage.setItem('access_token', response.data.access_token);
          localStorage.setItem('email', response.data.user.email);
          this.userData = (<any>response).data.user
          localStorage.setItem('userData', JSON.stringify(this.userData));
          return 'Success'

          
        })
        .catch(error => {
          console.error('There was an error submitting the data:', error.response.data);
          return error.response.data.detail
        });
      

    },
    logout(){
      // KADA CREDENTIALS EXPIRED THROW USER OUT FORM WEBSITE
      this.userLoggedIn = false
      this.setAuthToken = null
      this.setAuthTokenType = null
      this.setUserId = null
      this.setUsername = null
      localStorage.removeItem('access_token');
      localStorage.removeItem('email');
      localStorage.removeItem('userData');
    },
    async deleteUser(id:UserDelete) {
      
      axios.post(this.BASE_URL + 'user/delete/' + id, '',
      {
        headers: {
          'Authorization':'Bearer ' + localStorage.getItem('access_token'),
          'Accept': 'application/json'
        }
      })
        .then(response => {
          console.log(response.data);
          // window.location.reload(); // NE ZELIMO RELOADATI

        })
        .catch(error => {
          console.error(error);
          if(error.response.data.detail == 'Could not validate credentials'){
            this.logout()          
          }
        });
    },
    async updateUser(user:User){
      await axios.post(this.BASE_URL+'user/update/' + user.id, user,
        {
          headers: {
            'Authorization':'Bearer ' + localStorage.getItem('access_token'),
            'Accept': 'application/json',
            // 'Content-Type': 'json'//'multipart/form-data' 
          }
        })
          .then(response => {
            // Handle the response from the backend
            console.log('Form submitted successfully', response.data);
            // this.login_in_submission = true;
            // this.login_alert_variant = 'color: white; background-color:#339933; border: 1px solid #339933; box-shadow: 0 0 5px rgba(0,255,0,.3), 0 0 10px rgba(0,255,0,.2), 0 0 15px rgba(0,255,0,.1), 0 1px 0 #339933;';
            // this.login_alert_msg = 'Success! You have inserted new employ.';
          })
          .catch(error => {
            // Handle errors
            console.error('Error submitting form', error);
            if(error.response.data.detail == 'Could not validate credentials'){
              this.logout()          
            }
            // this.login_in_submission = true;
            // this.login_alert_variant = 'color: white; background-color:#990000;  border: 1px solid #990000;  box-shadow: 0 0 5px rgba(255,0,0,.3), 0 0 10px rgba(255,0,0,.2), 0 0 15px rgba(255,0,0,.1), 0 1px 0 #990000';
            // this.login_alert_msg = error.response.data.detail;
            return
          });
    },
    async insertUser(user:User){
      
      delete user['id'];
      
      console.log(user)
      
      await axios.post(this.BASE_URL+'user/create', user,
        {
          headers: {
            'Authorization':'Bearer ' + localStorage.getItem('access_token'),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            // 'Content-Type': 'multipart/form-data' 
          }
        })
          .then(response => {
            // Handle the response from the backend
            console.log('Form submitted successfully', response.data);
            
            // this.login_in_submission = true;
            // this.login_alert_variant = 'color: white; background-color:#339933; border: 1px solid #339933; box-shadow: 0 0 5px rgba(0,255,0,.3), 0 0 10px rgba(0,255,0,.2), 0 0 15px rgba(0,255,0,.1), 0 1px 0 #339933;';
            // this.login_alert_msg = 'Success! You have inserted new employ.';
          })
          .catch(error => {
            // Handle errors
            console.error('Error submitting form', error.response.status, error.response.data);

            console.error('Error submitting form', error);
            if(error.response.data.detail == 'Could not validate credentials'){
              this.logout()          
            }
            // this.login_in_submission = true;
            // this.login_alert_variant = 'color: white; background-color:#990000;  border: 1px solid #990000;  box-shadow: 0 0 5px rgba(255,0,0,.3), 0 0 10px rgba(255,0,0,.2), 0 0 15px rgba(255,0,0,.1), 0 1px 0 #990000';
            // this.login_alert_msg = error.response.data.detail;
            return
          });
    },
    async getUser(){
      try{
        const response = await axios.get(this.BASE_URL + 'user/'+window.location.pathname.split('/').pop(),
                                {
                                  headers: {
                                    'Authorization':'Bearer ' + localStorage.getItem('access_token'),
                                    'Accept': 'application/json'
                                  }
                                })
        return response.data;
      } catch (error) {
        console.error('There was an error:', (<any>error).response.data);
        if ((<any>error).response.data.detail == 'Could not validate credentials') {
          this.logout();
        }
        return {};
      }      
    },
    async uploadImage(image_name: string, images: any){

      const formData = new FormData();
      formData.append('images', images[0]);
      formData.append('name', image_name);
      console.log(formData)

      await axios.post(this.BASE_URL+'user/uploadImage', formData,
      {
        headers: {
          'Authorization':'Bearer ' + localStorage.getItem('access_token'),
          'Accept': 'application/json',
          'Content-Type': 'multipart/form-data' 
        }
      })
        .then(response => {
          // // Handle the response from the backend
          // console.log('Form submitted successfully', response.data);
          // this.login_in_submission = true;
          // this.login_alert_variant = 'color: white; background-color:#339933; border: 1px solid #339933; box-shadow: 0 0 5px rgba(0,255,0,.3), 0 0 10px rgba(0,255,0,.2), 0 0 15px rgba(0,255,0,.1), 0 1px 0 #339933;';
          // this.login_alert_msg = 'Success! You have inserted new post.';
        })
        .catch(error => {
          // // Handle errors
          // console.error('Error submitting form', error);
          // if(error.response.data.detail == 'Could not validate credentials'){
          //   this.logout()          
          // }
          // this.login_in_submission = true;
          // this.login_alert_variant = 'color: white; background-color:#990000;  border: 1px solid #990000;  box-shadow: 0 0 5px rgba(255,0,0,.3), 0 0 10px rgba(255,0,0,.2), 0 0 15px rgba(255,0,0,.1), 0 1px 0 #990000';
          // this.login_alert_msg = error.response.data.detail;
          // return
        });
    }
  }
})

