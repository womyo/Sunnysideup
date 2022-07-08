<template>
    <div>
        <v-col
        cols="12"
        sm="6"
        md="4"
        >
        <v-menu
            v-model="menu"
            :close-on-content-click="false"
            :nudge-right="40"
            transition="scale-transition"
            offset-y
            min-width="auto"
        >
            <template v-slot:activator="{ on, attrs }">
            <v-text-field
                v-model="date"
                label="Select date"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
            ></v-text-field>
            </template>
            <v-date-picker
            v-model="date"
            @input="menu = false"
            ></v-date-picker>
        </v-menu>
        </v-col>
        <!-- <v-btn color="primary" @click="getData">get data</v-btn> -->
    </div>
</template>

<script>
import axios from 'axios'

export default {
    'name': 'Sunriseset',
    data() {
        return {
            date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
            menu: false,
        }
    },

    mounted() {
        
    },
    methods: {
        async getData() {
            const url = `/city/서울/date/${this.formatDate(this.date)}`
            await axios
                .get(url)
                .then(response => {
                    console.log(response.data)
                })
                .catch(error => {
                        console.log(error)
                })
        },
        formatDate (date) {
            if (!date) return null

            const [year, month, day] = date.split('-')
            return `${year}${month}${day}`
        },
        
    }
}
</script>