<template>
    <div>
        <v-parallax v-if="this.image_link" height='350' class="placeImg" v-bind:style="{ backgroundImage: `url('${this.image_link}')` }">
            <h1 class="cityName"><span>{{ this.cityName }}</span></h1>
        </v-parallax>
        <div class="detail">
            <div class="sunrise">
                <img src="@/static/data/sunrise.svg"/>
                <p>{{ this.sunrise }}</p>
            </div>
            <div class="sunset">
                <img src="@/static/data/sunset.svg"/>
                <p>{{ this.sunset }}</p>
            </div>
        </div>
    </div>
</template>

<style lang="scss">
.placeImg {
    background: no-repeat center;
    background-size: cover;
    text-align: center;
}
.cityName {
    color: white;
}
.cityName span {
    background-color: rgba( 0, 0, 0, 0.2 );
}
.detail {
    text-align: center;
    margin-top: 20px;
    animation: motion 0.5s linear 0s infinite alternate; 
    margin-top: 0;
}
@keyframes motion {
	0% {margin-top: 0px;}
	100% {margin-top: 10px;}
}
.sunrise {
    display: inline-block;
    width: 20%;
    font-size:xx-large;
    font-family:'digital-clock-font';
}
.sunset {
    display: inline-block;
    width: 20%;
    margin-left: 15%;
    font-size:xx-large;
    font-family:'digital-clock-font';
}
</style>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            cityName: null,
            cityInfo: null,
            sunState: null,
            date: null,
            latitude: null,
            longitude: null,
            standard_time: null,
            image_link: null,
            sunrise: null,
            sunset: null,
        }
    },
    created() {
        this.cityName = this.$route.query.cityName
        this.sunState = this.$route.query.sunState
        this.date = this.$route.query.date
    },
    async mounted() {
        await this.getInfo()
        await this.getData()
    },
    methods: {
        async getInfo() {
            const url = `/api/${this.sunState}?name=${this.cityName}`

            await axios
                .get(url)
                .then(response => {
                    this.cityInfo = response.data[0]
                })
                .catch(error => {
                    console.log(error)
                })
        },
        async getData() {
            this.image_link = this.cityInfo.image_link
            this.latitude = this.cityInfo.latitude
            this.longitude = this.cityInfo.longitude
            this.standard_time = this.cityInfo.standard_time

            const url = `/date/${this.date}/lat/${this.latitude}/lon/${this.longitude}/standard/${this.standard_time}`
            
            await axios
                .get(url)
                .then(response => {
                    this.sunrise = response.data.sunrise
                    this.sunset = response.data.sunset
                })
                .catch(error => {
                        console.log(error)
                })
        }
  }
}
</script>