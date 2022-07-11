<template>
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
            Edit Place
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
                            :items="['rise', 'set']"
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
                            hint="The standard timezone used by the country"
                            persistent-hint
                            required
                            ></v-text-field>
                        </v-col>
                        <v-col
                            cols="12"
                        >
                            <v-text-field
                            ref="image_link"
                            v-model="image_link"
                            label="Image Url"
                            hint="Please make it empty if you want a Random Image"
                            persistent-hint
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
</template>

<script>
import axios from 'axios'

  export default {
    data: () => ({
      dialog: false,
      name: null,
      sun_state: null,
      latitude: null,
      longitude: null,
      standard_time: null,
      image_link: null,
      formHasErrors: false,
      url: null,
      cityInfo: null,
      image_link: null,
    }),
    computed: {
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
    created() {
        this.name = this.$route.query.cityName
        this.sun_state = this.$route.query.sunState
    },
    async mounted() {
        await this.getInfo()
        this.setData()
    },
    methods: {
        async getInfo() {
            await axios
                .get(`/api/${this.sun_state}?name=${this.name}`)
                .then(response => {
                    this.cityInfo = response.data[0]
                })
                .catch(error => {
                    console.log(error)
                })
        },

        setData() {
            this.image_link = this.cityInfo.image_link
            this.latitude = this.cityInfo.latitude
            this.longitude = this.cityInfo.longitude
            this.standard_time = this.cityInfo.standard_time
        },

        async submit () {
            this.formHasErrors = false
            this.dialog = false
            this.url = `/api/${this.sun_state}/?name=${this.name}`
            
            Object.keys(this.form).forEach(f => {
                if (!this.form[f]) {
                    this.formHasErrors = true
                    this.dialog = true
                }
                    this.$refs[f].validate(true)
                })

            const request_data = {
                'name': this.name,
                'latitude': this.latitude,
                'longitude': this.longitude,
                'standard_time': this.standard_time,
                'image_link': this.image_link
            }
            await axios
                .put(this.url, request_data)
                .then(resonse => {
                    console.log(resonse.data)
                })
                .catch(error => {
                    console.log(error)
                })
      },
    }
  }
</script>   