<template>
  <v-flex text-xs-center xs12>
    <div class="praise-code" v-show="praise">
      <img src="../assets/praise-code.jpg">
    </div>

    <footer class="caption">
      <p>更多惊喜,欢迎关注微信公众号
        <strong @click="$emit('click')" class="wechat-name">淘逗逗</strong>
      </p>
      <p>Created by
        <a href="javascript:void(0);" @click="praise=!praise">shellvon</a> |
        <a href="/feedback">使用反馈</a>
      </p>
    </footer>
  </v-flex>
</template>

<script>
export default {
  name: "FooterInfo",
  data() {
    return {
      praise: false
    };
  }
};
</script>

<style scoped>
footer {
  margin: 65px auto 0;
  color: #bfbfbf;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5);
}
footer > p {
  line-height: 1;
}
footer > p > a {
  color: #007acc;
  text-decoration: none;
}
.praise-code {
  margin-bottom: 30px;
}
.praise-code > img {
  border-radius: 2px;
  width: 100%;
}
.wechat-name {
  color: #007acc;
  cursor: pointer;
}
</style>
