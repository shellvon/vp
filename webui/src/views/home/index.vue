<template>
  <v-layout row wrap>
    <div class="logo">
      <img src="../../assets/logo.svg"/>
      <h1 class="primary--text display-5 font-weight-medium my-5">视频盒子</h1>
    </div>
    <v-flex text-xs-center xs12>
      <v-autocomplete
        v-model="selected"
        :items="items"
        :loading="loading"
        :search-input.sync="searchValue"
        @change="onSearch"
        clearable
        hide-selected
        item-text="title"
        item-value="title"
        label="搜索电影、电视剧、综艺、影人"
        solo
        flat
        return-object
       
      >

          <icon slot="prepend-inner" class="v-icon material-icons theme--light">search</icon>

        <template slot="no-data">
          <v-list-tile>
            <v-list-tile-title>
              输入你喜欢的
              <strong>演员or电影</strong>
            </v-list-tile-title>
          </v-list-tile>
        </template>

        <template slot="item" slot-scope="data">
          <template v-if="typeof data.item !== 'object'">
            <v-list-tile-content v-text="data.item"></v-list-tile-content>
          </template>
          <template v-else>
            <v-list-tile-avatar v-if="data.item.img">
              <img :src="`/dbimg?url=${data.item.img}`">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title v-html="data.item.title"></v-list-tile-title>
              <v-list-tile-sub-title v-html="data.item.type"></v-list-tile-sub-title>
            </v-list-tile-content>
          </template>
        </template>
      </v-autocomplete>

      <div class="text-xs-left mb-3" v-show="!searchValue">
        <v-chip text-color="#666" v-for="hot in hots" :key="hot.name"  color="#eee" class="clickable" @click="hotSearch(hot.name)">
            {{hot.name}}
        </v-chip>
      </div>
      <div class="qrcode" v-show="showQrCode">
        <p class="qr-title">可扫描屏幕下方二维码关注</p>
        <img src="../../assets/tdd-qr.png">
        <span class="tip">淘逗逗-视频盒子</span>
      </div>

      <v-card>
        <v-list xs12 class="pa-0">
          <template v-for="movie in movies">
            <movie-item :key="movie.id" :movie="movie"/>
            <v-divider :key="`${movie.id}-divider`" class="mb-4"></v-divider>
          </template>
        </v-list>
      </v-card>
    </v-flex>
    <v-snackbar
      v-model="snackbar"
      :color="'cyan darken-2'"
      :timeout="6000"
      :top="true"
    >没有搜到相关的视频,换个关键词试试吧....
      <v-btn dark flat @click="snackbar = false">关闭</v-btn>
    </v-snackbar>
    <footer-info v-on:click="showQrCode = !showQrCode"></footer-info>
  </v-layout>
</template>

<script>
import { throttle } from "@/utils/index";
import { suggest, search, getHotSearch } from "@/api/home";
import FooterInfo from "@/components/footerInfo";
import MovieItem from "@/components/movieItem";

export default {
  name: "Home",
  components: {
    FooterInfo,
    MovieItem
  },
  data() {
    return {
      snackbar: false,
      loading: false,
      showQrCode: false,
      suggestList: [],
      searchValue: "",
      selected: {},
      movies: [],
      hots: [],
    };
  },
  created() {
    getHotSearch().then(resp => {
      this.hots = resp;
    }).catch(e => {
      console.log(e)
    })
  },
  methods: {
    hotSearch(name) {
      this.selected = {title: name}
      this.searchValue = name
      this.onSearch()
    },
    onSearch() {
      if (!this.selected) {
        return;
      }
      this.showQrCode = false;
      this.loading = true;
      this.movies = [];
      this.$uweb.trackEvent('movie', 'search', this.selected.title)
      search(this.selected.title)
        .then(resp => {
          this.movies = resp;
        })
        .finally(() => {
          this.snackbar = this.movies.length === 0;
          this.loading = false;
        });
    },
    onSuggest: throttle(function(val) {
      if (this.loading) {
        return;
      }
      this.loading = true;
      suggest(val)
        .then(resp => {
          this.suggestList = resp;
        })
        .finally(() => {
          this.loading = false;
        });
    }, 500)
  },
  computed: {
    items() {
      let grouped = this.suggestList.reduce((r, a) => {
        r[a.type] = r[a.type] || [];
        r[a.type].push(a);
        return r;
      }, {});
      let result = this.searchValue ? [{ title: this.searchValue }] : [];
      for (var key in grouped) {
        if (!grouped[key].length) {
          continue;
        }
        if (!result) {
          result.push({ divider: true });
        }
        result.push({ header: key.toUpperCase() });
        result = result.concat(grouped[key]);
      }
      return result;
    }
  },
  watch: {
    searchValue(val) {
      this.onSuggest(val);
    }
  }
};
</script>

<style lang="scss">
.logo {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;

  img {
    margin-right: 10px;
    width: 48px;
    opacity: .7;
  }
}
h1 {
  opacity: 0.6;
}
.v-input__slot {
  border: 1px solid #eee;
}
.qrcode {
  background: #fff;
  border-radius: 2px;
  position: relative;
  .qr-title {
    font-size: 18px;
    // font-weight: 200;
    color: #fff;
    line-height: 50px;
    text-align: left;
    padding: 0 1em;
    box-sizing: border-box;
    background: rgb(33, 147, 204);
  }
  .tip {
    position: absolute;
    right: 5px;
    bottom: 5px;
    color: #999;
  }
}

.clickable {
  padding: 0 5px;
}
.clickable > .v-chip__content {
  cursor: pointer;
}
</style>
