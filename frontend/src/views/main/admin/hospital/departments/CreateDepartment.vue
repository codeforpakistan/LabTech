<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create Department</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Name" v-model="name" required></v-text-field>
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
  IHospital,
  IDepartmentCreate,
} from '@/interfaces';
import { dispatchGetHospitals, dispatchCreateHospitalDepartment } from '@/store/admin/actions';

@Component
export default class CreateHospitalDepartment extends Vue {
  public valid = false;
  public name: string = '';

  public async mounted() {
    await dispatchGetHospitals(this.$store);
    this.reset();
  }

  public reset() {
    this.name = '';
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedDepartment: IDepartmentCreate = {
        name: this.name,
        hospital_id: 1,
        owner_id: 1,
      };
      await dispatchCreateHospitalDepartment(this.$store, updatedDepartment);
      this.$router.push('/main/admin/hospital');
    }
  }
}
</script>
