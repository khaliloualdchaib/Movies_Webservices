<script lang="ts">
import axios from 'axios'
import TitleComponent from '../components/TitleComponent.vue'
export default {
    name: 'SearchPage',
    components: {
        TitleComponent
    },
    data() {
        return {
            searchquery: "",
            searchresults: [],
            loading: false,
            error: false,
            errormsg: "",
            optionselected: "",
            placeholder: "",
            deleted: false,
            movieiddeleted: 0,
            likedMovies: new Set<number>(),
        }
    },
    mounted() {
        this.fillLikedMovies()
    }
    ,
    methods: {
        ChoosePlaceHolder() {
            if (this.optionselected == "name") {
                this.placeholder = "Search a movie by name."
            } else if (this.optionselected == "id") {
                this.placeholder = "Search a movie by id."
            } else if (this.optionselected == "popular") {
                this.placeholder = "Give a number."
            } else if (this.optionselected == "genre" || this.optionselected == "actor" || this.optionselected == "runtime") {
                this.placeholder = "Give a movie id"
            }
        },
        isNonNegativeInteger(str: string) {
            if (/\D/.test(str)) {
                return false
            }
            return parseInt(str) >= 0;
        },
        async Like(id: number) {
            var url = 'http://127.0.0.1:5000/api/liked-movies/' + id;
            const response = await axios.post(url)
            if (response.status == 200) {
                this.likedMovies.add(id)
            }
        },
        async Unlike(id: number) {
            var url = 'http://127.0.0.1:5000/api/liked-movies/' + id;
            const response = await axios.delete(url)
            if (response.status == 200) {
                this.likedMovies.delete(id)
            }
        }
        ,
        async fillLikedMovies() {
            const url = 'http://127.0.0.1:5000/api/liked-movies';
            const resp = await axios.get(url)
            for (let i = 0; i<resp.data.data.length; i++){
                this.likedMovies.add(resp.data.data[i][0].id)
            }
        },
        async DELETE(id: number) {
            this.deleted = false
            var url = 'http://127.0.0.1:5000/api/movies/' + id;
            const response = await axios.delete(url);
            if (response.status == 200) {
                this.deleted = true
                this.movieiddeleted = id
                for (let i = 0; i < this.searchresults.length; i++) {
                    if (this.searchresults[i].id == id) {
                        this.searchresults.splice(i, 1);
                        return
                    }
                }
                return
            }
            this.error = true
            this.errormsg = "Movie Not Deleted."
        },
        async onSubmit() {
            try {
                this.error = false
                this.deleted = false
                console.log(this.optionselected)
                var url = 'http://127.0.0.1:5000/api/movies'
                if (this.optionselected == 'name') {
                    url += '?movie_title=' + this.searchquery
                } else if (!this.isNonNegativeInteger(this.searchquery)) {
                    this.error = true
                    this.errormsg = "Please enter a valid ID or number."
                    return
                } else if (this.optionselected == 'id') {
                    url += "/" + this.searchquery
                } else if (this.optionselected == 'popular') {
                    url += '/popular?limit=' + this.searchquery
                } else if (this.optionselected == "genre") {
                    url += "/" + this.searchquery + "/similar-genres"
                } else if (this.optionselected == "runtime") {
                    url += "/" + this.searchquery + "/similar-runtime"
                } else if (this.optionselected == "actor") {
                    url += "/" + this.searchquery + "/overlapping-actors"
                }
                this.loading = true
                const response = await axios.get(url);
                this.loading = false
                if (response.status != 200) {
                    this.error = true
                    this.errormsg = "There is no movie with the query you gave."
                    return
                }
                this.searchresults = response.data.data
            } catch (error) {
                this.loading = false
                this.error = true
                this.errormsg = "There is no movie with the query you gave."
                console.log(error)
            }
        },
        list2string(items: [string]) {
            var result = ''
            for (let i = 0; i < items.length; i++) {
                result += items[i] + ", "
            }
            result = result.slice(0, -2)
            return result
        }
    }
}

</script>

<template>
    <TitleComponent title="Search"></TitleComponent>
    <label for="options" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Select an option</label>
    <form class="flex items-center mb-10" @submit.prevent="onSubmit()">
        <select @change="ChoosePlaceHolder" required v-model="optionselected" id="options"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            <option value="name">Search movie by name</option>
            <option value="id">Search movie by ID</option>
            <option value="genre">Give movie ID, get movies with same genres</option>
            <option value="actor">Give movie ID, get movies with overlapping actors</option>
            <option value="runtime">Give movie ID, get movies with similar runtime</option>
            <option value="popular">Given a number(x), get first x popular movies </option>
        </select>
        <label for="simple-search" class="sr-only">Search</label>
        <div class="relative w-full">
            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor"
                    viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd"
                        d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                        clip-rule="evenodd"></path>
                </svg>
            </div>
            <input type="text" v-model="searchquery" id="simple-search"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                :placeholder="placeholder" required>
        </div>
        <button v-if="!loading" type="submit"
            class="p-2.5 ml-2 text-sm font-medium text-white bg-blue-700 rounded-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <span class="sr-only">Search</span>
        </button>
        <button disabled v-if="loading" type="submit"
            class="p-2.5 ml-2 text-sm font-medium text-white bg-blue-700 rounded-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            <div role="status">
                <svg aria-hidden="true" class="w-5 h-5 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                    viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                        fill="currentColor" />
                    <path
                        d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                        fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
            </div>
            <span class="sr-only">Search</span>
        </button>
    </form>
    <div class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" v-if="error"
        role="alert">
        <span class="font-medium">ERROR! {{ errormsg }}</span>
    </div>
    <div v-if="deleted" class="p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400"
        role="alert">
        <span class="font-medium">Movie {{ movieiddeleted }} deleted succesfully</span>
    </div>
    <div class="grid grid-cols-4 gap-4">
        <div v-for="movie in searchresults" v-bind:key="movie.id">
            <div class="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{{ movie.title }}</h5>
                <dl class="max-w-md text-gray-900 divide-y divide-gray-200 dark:text-white dark:divide-gray-700">
                    <div class="flex flex-col pb-3">
                        <dt class="mb-1 text-gray-500 md:text-lg dark:text-gray-400">id</dt>
                        <dd class="text-lg font-semibold">{{ movie.id }}</dd>
                    </div>
                    <div class="flex flex-col py-3">
                        <dt class="mb-1 text-gray-500 md:text-lg dark:text-gray-400">Actors</dt>
                        <dd class="text-lg font-semibold">{{ list2string(movie.actors) }}</dd>
                    </div>
                    <div class="flex flex-col py-3">
                        <dt class="mb-1 text-gray-500 md:text-lg dark:text-gray-400">Genres</dt>
                        <dd class="text-lg font-semibold">{{ list2string(movie.genres) }}</dd>
                    </div>
                    <div class="flex flex-col pt-3">
                        <button type="button" @click="DELETE(movie.id)"
                            class="focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900">DELETE</button>
                    </div>
                    <div class="flex flex-col pt-3">
                        <button @click="Unlike(movie.id)" v-if="likedMovies.has(movie.id)" type="button"
                            class="text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700">UNLIKE</button>
                        <button @click="Like(movie.id)" v-if="!likedMovies.has(movie.id)" type="button"
                            class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">LIKE</button>
                    </div>
                </dl>
            </div>
        </div>
    </div>
</template>