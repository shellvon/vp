<template>
  <v-layout row>
    <v-flex xs12>
      <v-snackbar
      v-model="snackbar"
      :color="'cyan darken-2'"
      :timeout="1500"
      :top="true"
    >已为您自动切换剧集
      <v-btn dark flat @click="snackbar = false">关闭</v-btn>
    </v-snackbar>

      <v-card>
        <v-progress-linear :indeterminate="true" v-if="loading" color="info"></v-progress-linear>
        <v-card-actions>
          <v-select :items="playlist" v-model="url" item-text="name" item-value="url" label="播放地址"></v-select>
          <v-spacer></v-spacer>
        </v-card-actions>

        <div class="player-container" v-if="playerType === 'm3u8'">
          <video-player ref="videoPlayer" class="vjs-custom-skin" :options="playerOptions" @ended="onPlayerEnded($event)"></video-player>
        </div>
        <div class="h_iframe" v-if="playerType === 'flash'">
          <iframe :src="url" frameborder="0" allowfullscreen></iframe>
        </div>
        <v-alert
          type="warning"
          :value="showWarning"
        >为了您的家庭幸福、财产安全、人生顺利，建议您不要去相信电影屏幕上的任何广告，单纯的享受观影带来的乐趣即可!</v-alert>

        <v-card-title primary-title>
          <div style="width: 100%;">
            <div class="headline movie-name">
              <span>{{movie.name}}</span>
              <v-icon color="orange" @click="showWarning = !showWarning">warning</v-icon>
            </div>
            <span class="grey--text small">{{movie.synopsis}}</span>
          </div>
        </v-card-title>
        <v-divider></v-divider>
        <v-slide-y-transition>
          <v-list v-if="show">
            <v-list-tile v-for="(val, key) in meta" :key="key">
              <v-list-tile-content>{{val}}:</v-list-tile-content>
              <v-list-tile-content class="align-end">{{ movie[key] }}</v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-slide-y-transition>
        <v-card-actions>
          <v-btn :to="{name: 'home'}" color="success" v-track-pageview="`/home,${$route.fullPath}`">返回搜索</v-btn>
          <v-dialog
            v-model="dialog"
            width="500"
            class="pl-1"
            v-if="movie.download_link && movie.download_link.length > 0"
          >
            <v-btn slot="activator" color="red lighten-2" dark>下载</v-btn>

            <v-card>
              <v-card-title class="headline grey lighten-2" primary-title>请选择你需要下载的片源</v-card-title>

              <v-card-text>
                <template v-if="movie.download_link && movie.download_link.length > 0">
                  <v-radio-group v-model="selected">
                    <v-radio
                      v-for="(item, key) in movie.download_link"
                      :key="key"
                      :value="item.url"
                    >
                      <div slot="label">
                        <a
                          :href="item.url"
                          class="download_link"
                          target="_blank"
                        >{{movie.name}}-{{item.name}}</a>
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
                <v-btn color="error" @click="download">下载</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-spacer></v-spacer>
          <v-btn icon @click="show = !show">
            <v-icon>{{ show ? 'keyboard_arrow_up' : 'keyboard_arrow_down' }}</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { videoPlayer } from "vue-video-player";

import { detail } from "@/api/home.js";

import "video.js/dist/video-js.css";
import "vue-video-player/src/custom-theme.css";
//引入hls.js
import "videojs-contrib-hls.js/src/videojs.hlsjs";

export default {
  name: "player",
  components: { videoPlayer },
  data() {
    return {
      loading: true,
      url: null,
      movie: {},
      playlist: [],
      playerType: "m3u8",
      show: false,
      dialog: false,
      snackbar: false,
      selected: "",
      episode: 1,
      totalEpisode: 1,
      showWarning: false,
      meta: {
        directors: "导演",
        actors: "主演",
        note: "备注",
        year: "年份",
        score: "评分"
      },
      playerOptions: {
        playbackRates: [0.7, 1.0, 1.5, 2.0, 5],
        autoplay: false,
        controls: true,
        preload: "auto",
        muted: false,
        loop: false,
        language: "zh-CN",
        aspectRatio: "16:9",
        fluid: true,
        sources: [],
        width: document.documentElement.clientWidth,
        notSupportedMessage: "此视频暂无法播放，请稍后再试"
      }
    };
  },
  beforeMount() {
    if (this.$route.query.url) {
      this.url = this.$route.query.url;
      let name = this.$route.query.name || this.url;
      this.playerType = this.url.indexOf(".m3u8") >= 0 ? "m3u8" : "flash";
      this.playlist = [{ name, url: this.url }];
      this.loading = false;
      return;
    }
    if (!this.$route.query.source || !this.$route.query.id) {
      this.$router.push({name: 'home'})
      return;
    }
    detail(this.$route.query.source, this.$route.query.id)
      .then(movie => {
        this.movie = movie;
        this.playerType = movie.play_m3u8.length ? "m3u8" : "flash";
        this.playlist =
          this.playerType === "m3u8" ? movie.play_m3u8 : movie.play_flash;
        if (this.playlist.length) {
          this.totalEpisode = this.playlist.length;
          this.episode = this.totalEpisode
          this.url = this.playlist[this.episode - 1].url
        }
      })
      .finally(() => (this.loading = false));
  },
  watch: {
    url() {
      this.playerOptions.sources = [{ src: this.url }];
      this.episode = this.playlist.findIndex(el => el.url === this.url) + 1
    }
  },
  methods: {
    download() {
      alert("Sorry, 暂未实现.");
    },
    onPlayerEnded(player)
    {
      this.snackbar = true;
      if (this.episode < this.totalEpisode) {
        this.episode ++;
      } else {
        this.episode = 1;
      }
      this.url = this.playlist[this.episode - 1].url;
      this.playerOptions.autoplay = true // 开启自动播放
    }
  }
};
</script>

<style lang="scss">
.h_iframe iframe {
  width: 100%;
  height: 56.25vw;
  max-height: 282px;
}
.movie-name {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
