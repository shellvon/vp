<template>
  <div class="page-feedback">
     <v-snackbar
      v-model="snackbar"
      :color="'cyan darken-2'"
      :timeout="6000"
      :top="true"
    >反馈成功
      <v-btn dark flat @click="snackbar = false">关闭</v-btn>
    </v-snackbar>

    <img src="./../../assets/bg@2x.png">
    <div class="content">
      <textarea v-model="form.content" cols="30" rows="6" placeholder="请填写10个字以上的意见或建议，我们将为你不断改进"></textarea>
    </div>
    <div class="form">
      <section>
        <span>邮箱</span>
        <input type="text" placeholder="（选填，方便我们答复你）" v-model="form.email">
      </section>
      <section>
        <span>微信号</span>
        <input type="text" placeholder="（选填，方便我们答复你）" v-model="form.weixin">
      </section>
      <section>
        <span>QQ号</span>
        <input type="text" placeholder="（选填，方便我们答复你）" v-model="form.qq">
      </section>
    </div>
    <button class="submit" @click="feedback" :disabled="!form.content">提交</button>
  </div>
</template>

<script>

import request from '@/utils/request'

export default {
  data () {
    return {
        snackbar: false,
        form: {
            content: '',
            weixin: '',
            email: '',
            qq: ''
        }
      
    }
  },
  created () {
    this.init()
  },
  methods: {
    init () {
      document.title = '视频盒子-意见反馈'
    },
    feedback () {
    
        request(this.form).then(() => {
            this.snackbar = true;
        }).catch(() => {
            this.snackbar = true;
        })
   
    }
  }
}
</script>

<style lang="scss" scoped>
.page-feedback {
  width: 100%;height: 100%;
  background: #F3F4F6;
  img {
    width: 100%;
    height: auto;
  }
  .content {
    background: #fff;
    textarea {
      background: #f3f4f6;
      border: 0;
      border-radius: 4px;
      resize: none;
      width: 90%;
      margin: 10px 5%;
      box-sizing: border-box;
      padding: 5px;
    }
  }
  .submit{
    background: #69D3C1;
    border-radius: 100px;
    width: 90%;
    margin: 15px 5%;
    border: 0;
    color: #fff;
    line-height: 36px;
    &[disabled] {
        background: rgb(175, 177, 177);
    }
  }
  .form {
    padding: 0 10px;
    box-sizing: border-box;
    line-height: 40px;
    background: #fff;
    & > section {
      display: flex;
      justify-content: space-between;
      align-items: center;
      span {
        width: 4em;
      }
      input {
        width: calc(#{"100% - 5em"});
      }
      &:not(:last-of-type){
        border-bottom: 1px solid #eee;
      }
    }
    input {
      border: 0;
      outline: none;
    }
  }
}
</style>
