<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Hospital</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Name" v-model="name" required></v-text-field>
            <v-text-field label="Address" type="text" v-model="address" required></v-text-field>
            <v-text-field label="latitude" type="text" v-model="lat" required></v-text-field>
            <v-text-field label="longitude" type="text" v-model="lng" required></v-text-field>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">
          Update
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
  import { Component, Vue } from 'vue-property-decorator';
  import { IHospitalUpdate } from '@/interfaces';
  import { dispatchGetHospitals, dispatchUpdateHospital } from '@/store/admin/actions';
  import { readAdminOneHospital } from '@/store/admin/getters';

  @Component
  export default class EditUser extends Vue {
    public valid = false;
    public name: string = '';
    public id: number = -1;
    public address: string = '';
    public lat: string = '';
    public lng: string = '';

    public async mounted() {
      await dispatchGetHospitals(this.$store, -1);
      this.id = parseInt(this.$router.currentRoute.params.id, 10);
      this.setData(this.hospital);
      this.reset();
    }

    public reset() {
      this.name = '';
      this.address = '';
      this.lat = '';
      this.lng = '';
      this.$validator.reset();
      if (this.hospital) {
        this.setData(this.hospital);
      }
    }

    public setData(hospital) {
      this.name = hospital?.name;
      this.id = hospital?.id;
      this.address = hospital?.address;
      this.lat = hospital?.lat;
      this.lng = hospital?.lng;
    }

    public cancel() {
      this.$router.back();
    }

    public async submit() {
      if (await this.$validator.validateAll()) {
        const updatedHopital: IHospitalUpdate = {
          id: this.id,
          name: this.name,
          address: this.address,
          lat: this.lat,
          lng: this.lng,
          create_date: new Date(),
        };
        await dispatchUpdateHospital(this.$store, {id: this.id, hospital: updatedHopital});
        this.$router.push('/main/admin/hospital');
      }
    }

    get hospital() {
      return readAdminOneHospital(this.$store)(+this.id);
    }

  }
</script>
