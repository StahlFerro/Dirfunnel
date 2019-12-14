<template>
<div>
    <MainPanel />
</div>
</template>

<script>
const remote = require("electron").remote;
const session = remote.getCurrentWebContents().session;

import { client } from "./vuecore/Client.vue";
import MainPanel from "./vuecore/MainPanel.vue";

var data = {

};

export default {
  name: "app",
  data: function() {
    return data;
  },
  components: {
    MainPanel,
  },
  methods: {
    // minimizeWindow: function () {
    //   var window = remote.getCurrentWindow();
    //   window.minimize();
    // },
    // exitApp: function() {
    //   var window = remote.getCurrentWindow();
    //   window.close();
    // }
  }
};
</script>
