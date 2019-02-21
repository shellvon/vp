<template>
    <footer class="caption">
        <p>更多惊喜,欢迎关注微信公众号<strong @click="$emit('click')" class="wechat-name">淘逗逗</strong></p>
        <p>Created by <a href="https://von.sh">shellvon</a> | <a href="/feedback">使用反馈</a></p>
    </footer>
</template>

<script>
export default {
    name: 'FooterInfo'
}
</script>

<style scoped>


footer {
    margin: 65px auto 0;
    color: #bfbfbf;
    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5)
}
footer > p {
    line-height: 1;
}
footer > p > a {
    color: #007acc;
    text-decoration: none
}
.wechat-name {
    color: #007acc;
}
</style>
