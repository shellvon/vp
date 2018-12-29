<template>
  <v-layout row>
    <v-flex xs12>
      <v-card>
        <v-card-actions>
          <v-select
            :items="movie.play_flash"
            v-model="movie.url"
            item-text="name"
            item-value="url"
            label="播放地址"
          ></v-select>
          <v-spacer></v-spacer>
        </v-card-actions>

        <div class="h_iframe">
          <iframe :src="movie.url" frameborder="0" allowfullscreen></iframe>
        </div>

        <v-card-title primary-title>
          <div>
            <div class="headline">{{movie.name}}</div>
            <span class="grey--text small">友情提示:由于微信的原因如果视频无法加载,请直接复制链接然后用浏览器打开即可播放.</span>
          </div>
        </v-card-title>
        <v-expansion-panel class="no-box-shadow">
          <v-expansion-panel-content v-for="(val, key) in meta" :key="key">
            <div slot="header">{{val}}:</div>
            <v-card>
              <v-card-text>{{movie[key]}}</v-card-text>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-card-actions>
          <v-btn :to="{name: 'home'}" color="success">返回搜索</v-btn>

   
          <v-dialog v-model="dialog" width="500" class="pl-1" v-if="movie.download_link">
            <v-btn slot="activator" color="red lighten-2" dark>下载</v-btn>

            <v-card>
              <v-card-title class="headline grey lighten-2" primary-title>请选择你需要下载的片源</v-card-title>

              <v-card-text>
                <template v-if="movie.download_link">
                  <v-radio-group v-model="selected">
                    <v-radio
                      v-for="(item, key) in movie.download_link"
                      :key="key"
                      :value="item.url"
                    >
                      <div slot="label">
                    
                        <a :href="item.url" class="download_link" target="_blank">{{movie.name}}-{{item.name}}</a>
                      </div>
                    </v-radio>
                  </v-radio-group>
                </template>
                <template v-else>暂无片源可供下载....</template>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                 <v-btn color="primary" @click="dialog = false">取消</v-btn>
                <v-btn color="error"  @click="download">下载</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-spacer></v-spacer>

          <!-- <v-btn icon @click="show = !show">简介
            <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
          </v-btn>-->
        </v-card-actions>

        <!-- <v-slide-y-transition>
          <v-card-text v-show="show" class="grey--text">{{movie.synopsis}}</v-card-text>
        </v-slide-y-transition>-->
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

import { mapState } from "vuex";

export default {
  name: "movie",
  data() {
    return {
      show: false,
      dialog: false,
      selected: "",
      meta: {
        name_alias: "影片别名",
        actors: "主演",
        directors: "导演",
        note: "备注",
        synopsis: "简介"
      }
    };
  },
  computed: {
    ...mapState({
      movie: state => state.movie.currentMovie
    })
  },
  methods: {
    download() {
      alert("请直接访问对应链接下载");
    }
  }
};
</script>

<style>
html,
body {
  height: 100%;
  width: 100%;
  margin: 0;
}
.h_iframe iframe {
  width: 100%;
  height: 100%;
  background-color: cadetblue;
}
.h_iframe {
  height: 100%;
  width: 100%;
}
span.small {
  font-size: 10px;
}
.no-box-shadow {
  box-shadow: none;
  -webkit-box-shadow: none;
}
.download_link {
    color: #007acc;
    opacity: 0.8;
    text-decoration: none;
}
</style>
