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
            <v-select
            v-if="!addNewModule"
                v-model="moduleName"
                :items="options"
                label="Select Module Name"
                persistent-hint
                return-object
                single-line
                clearable
                v-on:change="onModuleChange(moduleName)"
              >
              </v-select>
          </v-form>
          <v-text-field v-if="addNewModule" label="Module Name" v-model="moduleName" required></v-text-field>
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
import { dispatchCreateHospitalDepartment, dispatchGetModuleNames } from '@/store/admin/actions';
import { readUserProfile } from '@/store/main/getters';
import { readModuleNames } from '@/store/admin/getters';

@Component
export default class CreateHospitalDepartment extends Vue {
  public valid = false;
  public addNewModule: boolean = false
  public name: string = '';
  public options:any = [];
  public moduleName: string = '';
  private id: number = -1;

  public async mounted() {
    await dispatchGetModuleNames(this.$store);
    this.options = this.moduleNames?.modules;
    this.options.push('Add New');
    this.id = parseInt(this.$router.currentRoute.params.id, 10);
    this.reset();
  }

  onModuleChange(select) {
    if (select === 'Add New') {
      this.addNewModule = true;
      this.moduleName = '';
    }
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
    this.$router.push('/main/admin/lab/' + this.id);
    return;
  }

  get userProfile() {
    return readUserProfile(this.$store);
  }

  get moduleNames() {
    return readModuleNames(this.$store);
  }
}
</script>
