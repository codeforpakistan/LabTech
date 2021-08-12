<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create Lab</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Name" v-model="name" required></v-text-field>
            <v-text-field label="Address" type="text" v-model="address" required></v-text-field>
            <v-checkbox
              label="Copy default indicators and survey questions"
              v-model="isCreateWithDefault"
            ></v-checkbox>
            <!-- <v-text-field label="latitude" type="text" v-model="lat" required></v-text-field>
            <v-text-field label="longitude" type="text" v-model="lng" required></v-text-field> -->
            <!-- <div class="mt-3">
              <v-label>Select Type</v-label>
              <v-select
                v-model="hospitalType"
                :items="types"
                item-text="name"
                item-value="name"
                label="Select Hospital type"
                persistent-hint
                single-line
                clearable
              >
            </v-select>
            </div> -->
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">
              Save
            </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  IHospitalCreate,
} from '@/interfaces';
import { dispatchGetHospitals, dispatchCreateHospital } from '@/store/admin/actions';
import { readUserProfile } from '@/store/main/getters';

@Component
export default class CreateHospital extends Vue {
  public valid = false;
  public name: string = '';
  public hospitalType: string = '';
  public isCreateWithDefault: boolean = true;
  public address: string = '';
  public lat: string = '';
  public lng: string = '';
  public types = ['BHU', 'HOSPITAL', 'OTHER'];

  public async mounted() {
    await dispatchGetHospitals(this.$store);
    this.reset();
  }

  public reset() {
    this.name = '';
    this.address = '';
    this.lat = '';
    this.lng = '';
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedHopital: IHospitalCreate = {
        name: this.name,
        address: this.address || 'abc',
        lat: this.lat || '1.0',
        lng: this.lng || '1.0',
        create_date: new Date(),
        owner_id: this.userProfile?.id || -1,
        hospital_type: this.hospitalType ? this.hospitalType.toUpperCase() : 'OTHER',
        isCreateWithDefault: this.isCreateWithDefault,
      };
      await dispatchCreateHospital(this.$store, updatedHopital);
      this.$router.push('/main/admin/lab');
    }
  }

  get userProfile() {
    return readUserProfile(this.$store);
  }
}
</script>
