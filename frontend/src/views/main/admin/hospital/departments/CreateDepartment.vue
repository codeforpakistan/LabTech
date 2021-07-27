<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create Indicator</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Name" v-model="name" required></v-text-field>
            <v-text-field label="Module Name" v-model="moduleName" required></v-text-field>
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
import { IDepartmentCreate } from '@/interfaces';
import { dispatchCreateHospitalDepartment } from '@/store/admin/actions';
import { readUserProfile } from '@/store/main/getters';

@Component
export default class CreateHospitalDepartment extends Vue {
  public valid = false;
  public name: string = '';
  public moduleName: string = '';
  private id: number = -1;

  public async mounted() {
    this.id = parseInt(this.$router.currentRoute.params.id, 10);
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
    const updatedDepartment: IDepartmentCreate = {
      module_name: this.moduleName,
      name: this.name,
      hospital_id: this.id,
      owner_id: this.userProfile?.id || -1,
    };
    await dispatchCreateHospitalDepartment(this.$store, updatedDepartment);
    this.$router.push('/main/admin/hospital/' + this.id);
    return;
  }

  get userProfile() {
    return readUserProfile(this.$store);
  }
}
</script>
