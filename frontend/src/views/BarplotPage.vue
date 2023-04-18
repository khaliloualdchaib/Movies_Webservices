<script lang="ts">
import TitleComponent from '../components/TitleComponent.vue'
import axios from 'axios'

export default {
    name: 'BarplotPage',
    components: {
        TitleComponent
    },
    data() {
        return {
            inputerror: false,
            errormsg: "",
            input: "",
            loading: false,
            URL: "",
        }
    },
    methods: {
        validateInput() {
            // Regular expression to match the desired input format
            const regex = /^\d+(,\s*\d+)*$|^\d+$/;
            this.inputerror = false
            if (!this.input.match(regex)) {
                this.inputerror = true
                this.errormsg = "Please give a valid input of the form id1, id2, id3, ..."
            }
        },
        async onSubmit() {
            try {
                this.loading = true
                this.inputerror = false
                this.validateInput()
                if (this.inputerror) {
                    return
                }
                const url = "http://127.0.0.1:5000/api/movies/barplot?movies=" + this.input
                const response = await axios.get(url);
                if (response.status == 200) {
                    console.log('test')
                    this.URL = response.data.data
                    this.loading = false
                    return
                }
            } catch (error) {
                this.inputerror = true
                this.loading = false
                this.errormsg = ""
                console.log(error)
            }
        }

    }
}

</script>

<template>
    <TitleComponent title="Barplot"></TitleComponent>

    <form @submit.prevent="onSubmit()">
        <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
        <div class="relative">
            <input v-model="input" type="search" id="default-search"
                class="block w-full p-4 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="MovieID1, MovieID2, MovieID3, ..." required>
            <button v-if="!loading" type="submit"
                class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Generate</button>
            <button disabled v-if="loading" type="submit"
                class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
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
            </button>
        </div>
    </form>
    <div class="p-4 mt-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400"
        v-if="inputerror" role="alert">
        <span class="font-medium">ERROR! {{ errormsg }}</span>
    </div>
    <img :src="URL" alt="">
</template>