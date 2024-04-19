APP_VUE_BOILERPLATE = """<template>
	<div>
		<button v-if="$auth.isLoggedIn" @click="$auth.logout()">Logout</button>
		<router-view />
	</div>
</template>


<script>
export default {
	inject: ['$auth']
};
</script>
"""

HOME_VUE_BOILERPLATE = """<template>
  <div>
    <h1>Home Page</h1>
    <!-- Fetch the resource on click -->
    <button @click="$resources.ping.fetch()">Ping</button>
  </div>
</template>

<script>
export default {
  resources: {
    ping() {
      return {
        method: "frappe.ping", // Method to call on backend
        onSuccess(d) {
          alert(d);
        },
      };
    },
  },
};
</script>
"""

LOGIN_VUE_BOILERPLATE = """<template>
  <div class="min-h-screen bg-white flex">
    <div class="mx-auto w-full max-w-sm lg:w-96">
      <form @submit.prevent="login" class="space-y-6">
        <label for="email"> Username: </label>
        <input type="text" v-model="email" />
        <br />
        <label for="password"> Password: </label>
        <input type="password" v-model="password" />

        <button
          class="bg-blue-500 block text-white p-2 hover:bg-blue-700"
          type="submit"
        >
          Sign in
        </button>
      </form>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      email: null,
      password: null,
    };
  },
  inject: ["$auth"],
  async mounted() {
    if (this.$route?.query?.route) {
      this.redirect_route = this.$route.query.route;
      this.$router.replace({ query: null });
    }
  },
  methods: {
    async login() {
      if (this.email && this.password) {
        let res = await this.$auth.login(this.email, this.password);
        if (res) {
          this.$router.push({ name: "Home" });
        }
      }
    },
  },
};
</script>
"""

VUE_VITE_CONFIG_BOILERPLATE = """import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import proxyOptions from './proxyOptions';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	server: {
		port: 8080,
		proxy: proxyOptions
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src')
		}
	},
	build: {
		outDir: '../{{app}}/public/{{name}}',
		emptyOutDir: true,
		target: 'es2015',
	},
});
"""

PROXY_OPTIONS_BOILERPLATE = """const common_site_config = require('../../../sites/common_site_config.json');
const { webserver_port } = common_site_config;

export default {
	'^/(app|api|assets|files)': {
		target: `http://localhost:${webserver_port}`,
		ws: true,
		router: function(req) {
			const site_name = req.headers.host.split(':')[0];
			return `http://${site_name}:${webserver_port}`;
		}
	}
};
"""

MAIN_JS_BOILERPLATE = """import { createApp, reactive } from "vue";
import App from "./App.vue";

import router from './router';
import resourceManager from "../../../doppio/libs/resourceManager";
import call from "../../../doppio/libs/controllers/call";
import socket from "../../../doppio/libs/controllers/socket";
import Auth from "../../../doppio/libs/controllers/auth";

const app = createApp(App);
const auth = reactive(new Auth());

// Plugins
app.use(router);
app.use(resourceManager);

// Global Properties,
// components can inject this
app.provide("$auth", auth);
app.provide("$call", call);
app.provide("$socket", socket);


// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	if (to.matched.some((record) => !record.meta.isLoginPage)) {
		// this route requires auth, check if logged in
		// if not, redirect to login page.
		if (!auth.isLoggedIn) {
			next({ name: 'Login', query: { route: to.path } });
		} else {
			next();
		}
	} else {
		if (auth.isLoggedIn) {
			next({ name: 'Home' });
		} else {
			next();
		}
	}
});

app.mount("#app");
"""

ROUTER_INDEX_BOILERPLATE = """import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import authRoutes from './auth';

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  ...authRoutes,
];

const router = createRouter({
  base: "/{{name}}/",
  history: createWebHistory(),
  routes,
});

export default router;
"""


AUTH_ROUTES_BOILERPLATE = """export default [
    {
		path: '/login',
		name: 'Login',
		component: () =>
			import(/* webpackChunkName: "login" */ '../views/Login.vue'),
		meta: {
			isLoginPage: true
		},
		props: true
	}
]
"""

REACT_VITE_CONFIG_BOILERPLATE = """import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react'
import proxyOptions from './proxyOptions';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		port: 8080,
		proxy: proxyOptions
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src')
		}
	},
	build: {
		outDir: '../{{app}}/public/{{name}}',
		emptyOutDir: true,
		target: 'es2015',
	},
});
"""

APP_REACT_BOILERPLATE = """import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { FrappeProvider } from 'frappe-react-sdk'
function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <FrappeProvider>
        <div>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src="/vite.svg" className="logo" alt="Vite logo" />
        </a>
        <a href="https://reactjs.org" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React + Frappe</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      </div>
      </FrappeProvider>
    </div>
  )
}

export default App
"""