<template>
    <div>
        <v-row>
            <v-col
                cols="12"
                sm="6"  
                md="3"
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
                    :allowed-dates="disableFutureDate"
                    @input="menu = false"
                    ></v-date-picker>
                </v-menu>
            </v-col>
        </v-row>
        <v-dialog
        v-model="dialog"
        persistent
        max-width="600px"
        >
        <template v-slot:activator="{ on, attrs }">
            <v-btn
            color="primary"
            dark
            v-bind="attrs"
            v-on="on"
            >
            Add Place
            </v-btn>
        </template>
        <v-card ref="form">
            <v-card-title>
                <span class="text-h5">Place Info</span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col 
                            cols="12"
                            sm="9">
                            <v-text-field
                            ref="name"
                            v-model="name"
                            :rules="[() => !!name || 'This field is required']"
                            label="Name*"
                            hint="Place, Country"
                            required
                            ></v-text-field>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="3"
                        >
                            <v-select
                            ref="sun_state"
                            v-model="sun_state"
                            :rules="[() => !!sun_state|| 'This field is required']"
                            :items="['Rise', 'Set']"
                            label="Sun State*"
                            required
                            ></v-select>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            ref="latitude"
                            v-model="latitude"
                            :rules="[() => !!latitude || 'This field is required']"
                            label="Latitude*"
                            required
                            ></v-text-field>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            ref="longitude"
                            v-model="longitude"
                            :rules="[() => !!longitude || 'This field is required']"
                            label="Longitude*"
                            required
                            ></v-text-field>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            ref="standard_time"
                            v-model="standard_time"
                            :rules="[() => !!standard_time || 'This field is required']"
                            label="Standard Time*"
                            hint="The standard time longitude used by the country"
                            persistent-hint
                            required
                            ></v-text-field>
                        </v-col>
                    </v-row>
                </v-container>  
                <small>*indicates required field</small>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="blue darken-1"
                    text
                    @click="dialog = false"
                >
                    Close
                </v-btn>
                <v-btn
                    color="blue darken-1"
                    text
                    @click="submit"
                >
                    Save
                </v-btn>
            </v-card-actions>
        </v-card>
        </v-dialog>
        <v-row>
            <v-col id="map-wrapper" class="map-wrapper">
                <div class='box' v-show="upHere" :style="{left:xPosition, top:yPosition}" >
                    <div>{{ this.cityName }}</div>
                    <div>{{ this.sunrise }}</div>
                    <div>{{ this.sunset }}</div>
                </div>
            </v-col >
        </v-row>

    </div>
</template>


<style lang="scss">
.map-wrapper {
    display: flex;
    position:relative;
    text-align: center;

  .background {
    // fill: #021019; 
    fill: transparent;
    pointer-events: all;
  }
  
  .map-layer {
    // fill: #08304b;
    stroke: #021019;
    stroke-width: 1px;
  }
  .box {
    display: flex;
    position: absolute;
    background-color: black;
    color: white;   
  }
}
</style>

<script>
import * as d3 from 'd3'
import axios from 'axios'
import { mapGetters, mapActions } from 'vuex'

const MAP_GEOJSON = require('../static/data/custom.geo.json');

export default {
  components: {
  },
  props: {
  },
  data() {
    return {
        date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        menu: false,
        upHere : false,
        xPosition: 0,
        yPosition: 0,
        cityName: '',
        sunrise: '',
        sunset: '',
        resData: {},
        riseInfo: [],
        setInfo: [],
        province: undefined,
        currentProvince: undefined,
        localSeatInfo : null,

        dialog: false,
      name: null,
      sun_state: null,
      latitude: null,
      longitude: null,
      standard_time: null,
      formHasErrors: false,
      url: null,
    }
  },
  created() {
    this.$store.dispatch('getRiseInfo')
  },
  computed: {
    // ...mapGetters(["storeRiseInfo"])
    form () {
        return {
          name: this.name,
          sun_state: this.sun_state,
          latitude: this.latitude,
          longitude: this.longitude,
          standard_time: this.standard_time,
        }
      },
  },
  async mounted() {
    // await this.$store.dispatch('getRiseInfo')
    // console.log(...mapGetters(["storeRiseInfo"]))
    // console.log(this.$store.state.riseInfo)
    await axios
        .get('/api/rise/')
        .then(response => {
            this.riseInfo = response.data
        })
        .catch(error => {
            console.log(error)
        })
    await axios
        .get('/api/set/')
        .then(response => {
            this.setInfo = response.data
        })
        .catch(error => {
            console.log(error)
        })
    this.drawMap(); 
  },
  methods: {
    async submit () {
            this.formHasErrors = false
            this.dialog = false
            
            Object.keys(this.form).forEach(f => {
                if (!this.form[f]) {
                    this.formHasErrors = true
                    this.dialog = true
                }
                    this.$refs[f].validate(true)
                })

            // 저장
            if (this.sun_state == "Rise") {
                this.url = '/api/rise/'
            }
            else {
                this.url = '/api/set/'
            }
            const request_data = {
                'name': this.name,
                'latitude': this.latitude,
                'longitude': this.longitude,
                'standard_time': this.standard_time
            }
            await axios
                .post(this.url, request_data)
                .then(resonse => {
                    console.log(resonse.data)
                })
                .catch(error => {
                    console.log(error)
                })

            if (!this.formHasErrors & !this.dialog){
                Object.keys(this.form).forEach(f => {
                    this.$refs[f].reset()
                })
            }
            await axios
                .get('/api/rise/')
                .then(response => {
                    this.riseInfo = response.data
                })
                .catch(error => {
                    console.log(error)
                })
            await axios
                .get('/api/set/')
                .then(response => {
                    this.setInfo = response.data
                })
                .catch(error => {
                    console.log(error)
                })

      },
    disableFutureDate(val) {
        return val >= new Date().toISOString().substr(0, 10)
    },
    async getData(lat, lon, standard) {
        const url = `/date/${this.formatDate(this.date)}/lat/${lat}/lon/${lon}/standard/${standard}`
        await axios
            .get(url)
            .then(response => {
                this.resData = response.data
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

    async drawMap() {
        const geojson = MAP_GEOJSON;
        // 지도의 중심점 찾기
        const center = d3.geoCentroid(geojson);

        let centered = undefined;

        // 현재의 브라우저의 크기 계산
        const divWidth = document.getElementById("map-wrapper").clientWidth;
        const width = divWidth
        const height = width * 0.5;

        // 지도를 그리기 위한 svg 생성
        const svg = d3
        // .select('.d3')
            .select('.map-wrapper')
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        // 배경 그리기
        const background = svg.append('rect')
            .attr('class', 'background')
            .attr('width', width)
            .attr('height', height)

        // 지도가 그려지는 그래픽 노드(g) 생성
        const g = svg.append('g');
        // 지도가 그려지는 그래픽 노드
        const mapLayer = g.append('g').classed('map-layer', true);
        // 아이콘이 그려지는 그래픽 노드
        const riseIcon = g.append('g').classed('rise-icon', true);
        const setIcon = g.append('g').classed('set-icon', true);

        // 지도의 출력 방법을 선택(메로카토르)
        var projection = d3.geoMercator()
            .scale(1)
            .translate([0, 0]); 

        // svg 그림의 크기에 따라 출력될 지도의 크기를 다시 계산
        const path = d3.geoPath().projection(projection);
        const bounds = path.bounds(geojson);
        const widthScale = (bounds[1][0] - bounds[0][0]) / width; 
        const heightScale = (bounds[1][1] - bounds[0][1]) / height; 
        const scale = 0.95 / Math.max(widthScale, heightScale);
        const xoffset = width/2 - scale * (bounds[1][0] + bounds[0][0]) /2 + 0; 
        const yoffset = height/2 - scale * (bounds[1][1] + bounds[0][1])/2 + 0; 
        const offset = [xoffset, yoffset];
        projection.scale(scale).translate(offset);


        const color = d3.scaleLinear()
            .domain([1, 20])
            .clamp(true)
            .range(['#595959', '#595959']);

        // Get province name length
        function nameLength(d){
            const n = nameFn(d);
            return n ? n.length : 0;
        }

        // Get province name
        function nameFn(d){
            return d && d.properties ? d.properties.name : null;
        }
        
        // Get province color
        function fillFn(d){
            return color(nameLength(d));
        }


        // 지도 그리기
        mapLayer
            .selectAll('path')
            .data(geojson.features)
            .enter().append('path') 
            .attr('d', path)
            .attr('vector-effect', 'non-scaling-stroke')
            .style('fill', fillFn);


        const riseInfo = [
            {
                "name": "Angkor Wat, Cambodia",
                "latitude": 13.40749837,
                "longitude": 103.8666632,
                "standard_time": 105.0
            },
            {
                "name": "Seongsan Ilchulbong, Korea",
                "latitude": 33.458428,
                "longitude": 126.939898,
                "standard_time": 135.0
            },
            {'name': 'Taj Mahal, India', 'latitude': '27.173891', 'longitude': '78.042068', 'standard_time': '82.5'},
            {'name': 'Ananda Temple, Myanmar', 'lat': '21.170582', 'lon': '94.866615', 'standard': '97.5'},
            {'name': 'Koh Lipe, Thailand', 'lat': '6.486963', 'lon': '99.310219', 'standard': '105'},
            {'name': 'Moraine Lake, Canada', 'lat': '51.328239', 'lon': '-116.181717', 'standard': '-90'},
            {'name': 'Haleakalā Crater, USA', 'lat': '20.7186111', 'lon': '-156.1827778', 'standard': '-150'},
            {'name': 'Borobudur Temple, Indonesia', 'lat': '-7.607355', 'lon': '110.203804', 'standard': '105'},
            {'name': 'Grand Canyon, USA', 'lat': '36.056595', 'lon': '-112.125092', 'standard': '-105'},
            {'name': 'uluru, Austrailia', 'lat': '-25.344490', 'lon': '131.035431', 'standard': '142.5'},
            {'name': 'Sarangkot, Nepal', 'lat': '28.270939', 'lon': '83.915676', 'standard': '86.25'},
            {'name': 'Cadillac Mountain, USA', 'lat': '44.3505', 'lon': '-68.2223', 'standard': '-60'},
            // {'name': 'Pico do Papagaio, Brazil', 'lat': '-7.8232', 'lon': '-38.055867', 'standard': '-45'},
            // {'name': 'Stonehenge, United Kingdom', 'lat': '51.1740', 'lon': '-1.8224', 'standard': '15'},
            // {'name': 'Park Güell, Spain', 'lat': '41.414494', 'lon': '2.152695', 'standard': '30'},
            // {'name': 'Mount Kenya, Kenya', 'lat': '-0.16666666666667', 'lon': '37.299722222222', 'standard': '45'},
            // {'name': 'Mount Kilimanjaro, Tanzania', 'lat': '-3.065653', 'lon': '37.352013', 'standard': '45'},
            // {'name': 'Avenue of the Baobabs, Madagascar', 'lat': '-20.2498', 'lon': '44.4194', 'standard': '45'},
            // {'name': 'The Little Mermaid, Denmark', 'lat': '55.6890', 'lon': '12.5929', 'standard': '30'},
            // {'name': 'Matterhorn, Switzerland', 'lat': '45.980537', 'lon': '7.641618', 'standard': '30'},
            // {'name': 'Halászbástya, Hungary', 'lat': '47.501896', 'lon': '19.035133', 'standard': '30'},
            // {'name': 'Kamari, Greece', 'lat': '36.3727', 'lon': '25.4758', 'standard': '45'},
            // {'name': 'Charles Bridge, Czech Republic', 'lat': '50.0852013259', 'lon': '14.4071117049', 'standard': '30'},
            // {'name': 'Geysers Del Tatio, Chile', 'lat': '-22.334791', 'lon': '-68.013077', 'standard': '-60'},
            // {'name': 'Punta Sur, Mexico', 'lat': '25.641927', 'lon': '-100.279474', 'standard': '-75'},
            // {'name': 'Huangshan, China', 'lat': '29.7114', 'lon': '118.3125', 'standard': '120'},
            // {'name': 'Jebel Fihrayn, Saudi Arabia', 'lat': '24.93124', 'lon': '45.98367', 'standard': '45'},
        ]

        const setInfo = [
            {'name': 'Mallory Square, USA', 'lat': '24.5600', 'lon': '-81.8074', 'standard': '-60'},
            {'name': 'Burj Khalifa, Dubai', 'lat': '25.197525', 'lon': '55.274288', 'standard': '60'},
            {'name': 'Piazzale Michelangelo, Italy', 'lat': '43.7577', 'lon': '11.2591', 'standard': '30'},
            {'name': 'Tanah Lot, Indonesia', 'lat': '-8.6400', 'lon': '115.1000', 'standard': '120'},
            {'name': 'Mindil Beach, Austrailia', 'lat': '-12.445589', 'lon': '130.830835', 'standard': '142.5'},
            {'name': 'Eiffel Tower, France', 'lat': '48.858093', 'lon': '2.294694', 'standard': '30'},
            {'name': 'N Seoul Tower, Korea', 'lat': 37.5508527966, 'lon': 126.986129389, 'standard': 135},
            {'name': 'Itchan Kala, Uzbekistan', 'lat': '41.378', 'lon': '60.364', 'standard': '75'},
            {'name': 'Empire State Building, USA', 'lat': '40.748817', 'lon': '-73.985428', 'standard': '-60'},
            {'name': 'Museo – Taller de Casapueblo, Uruguay', 'lat': '-34.90868', 'lon': '-55.044792', 'standard': '-45'},
            {'name': 'Miraflores, Peru', 'lat': '-12.117880', 'lon': '-77.033043', 'standard': '-75'},
            {'name': 'Sun Voyager, Iceland', 'lat': '64.1419', 'lon': '-21.9200', 'standard': '0'},
            {'name': 'Sea Fortress Suomenlinna, Finland', 'lat': '60.148884', 'lon': '24.984615', 'standard': '45'},
            {'name': 'Fushimi Inari-taisha, Japan', 'lat': '34.966996132', 'lon': '135.770330252', 'standard': '135'},
            {'name': 'Flaming Cliffs, Mongolia', 'lat': '44.1364', 'lon': '103.7233', 'standard': '120'},
            {'name': 'Tashichho Dzong, Bhutan', 'lat': '27.4870', 'lon': '89.6343', 'standard': '90'},
            {'name': 'Temple of Debod, Spain', 'lat': '40.4210966489', 'lon': '-3.717330464', 'standard': '30'},
            {'name': 'Galle Face Green, Sri Lanka', 'lat': '6.9266', 'lon': '79.8435', 'standard': '82.5'},
            {'name': 'CN Tower, Canada', 'lat': '43.642567', 'lon': '-79.387054', 'standard': '-60'},
            {'name': 'Kingdom Centre, Saudi Arabia', 'lat': '24.7068', 'lon': '46.6713', 'standard': '45'},
            {'name': 'Signal Hill (Cape Town), South Africa', 'lat': '-33.917329664', 'lon': '18.40166506', 'standard': '30'},
            {'name': 'Labadi Pleasure Beach, Ghana', 'lat': '5.561919', 'lon': '-0.139747', 'standard': '0'},
            {'name': 'Agadir, Morocco', 'lat': '30.410753', 'lon': '-9.604345', 'standard': '15'},

        ]


        await riseIcon
        .selectAll('svg')
        .data(this.riseInfo)
        .enter()  
        .append("svg:image")
        .attr("width", 30)
        .attr("height", 30)
        .attr('x' ,  d=> projection([d.longitude-2, d.latitude])[0])
        .attr('y' ,  d=> projection([d.longitude, d.latitude-(-2)])[1])
        .attr("xlink:href", require("../static/data/sunrise.svg")) 
        .on('mouseover', d =>{
            this.upHere = true
            this.xPosition = (d.pageX)  + 'px'
            this.yPosition = (d.pageY - 100)+ 'px'
            const target =  d.target.__data__
            this.cityName = target.name
            this.getData(target.latitude, target.longitude, target.standard_time)
            this.sunrise = this.resData.sunrise
            this.sunset = this.resData.sunset
        })
        .on('mouseleave', d =>{
            this.upHere = false
        })
        .on('click', d =>{
            this.getData(d.target.__data__.name)
        })

        await setIcon
        .selectAll('svg')
        .data(this.setInfo)
        .enter()  
        .append("svg:image")
        .attr("width", 30)
        .attr("height", 30)
        .attr('x' ,  d=> projection([d.longitude-2, d.latitude])[0])
        .attr('y' ,  d=> projection([d.longitude, d.latitude-(-2)])[1])
        .attr("xlink:href", require("../static/data/sunset.svg")) 
        .on('mouseover', d =>{
            this.upHere = true
            this.xPosition = (d.pageX)  + 'px'
            this.yPosition = (d.pageY - 100)+ 'px'
            const target =  d.target.__data__
            this.cityName = target.name
            this.getData(target.latitude, target.longitude, target.standard_time)
            this.sunrise = this.resData.sunrise
            this.sunset = this.resData.sunset
        })
        .on('mouseleave', d =>{
            this.upHere = false
        })
        .on('click', d =>{
            this.getData(d.target.__data__.name)
        })

        // function projection(point) {
        //     return 1
        //     // point = projectRotate(point[0] * __WEBPACK_IMPORTED_MODULE_5__math__["r" /* radians */], point[1] * __WEBPACK_IMPORTED_MODULE_5__math__["r" /* radians */]);
        //     // return [point[0] * k + dx, dy - point[1] * k];
        // }

        // svg.call(d3.zoom().duration(1000)
        // .on("zoom", function () {
        //     svg.attr("transform", d3.zoomTransform(this))
        // }))
        // .on("wheel.drag", null);
    },
  }
}

</script>