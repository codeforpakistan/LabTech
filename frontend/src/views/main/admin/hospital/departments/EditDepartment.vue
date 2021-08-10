<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Indicator</div>
      </v-card-title>
      <v-card-text>
      <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Name" v-model="name" required></v-text-field>
            <v-select
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
          <v-text-field v-if="addNewModule" label="Module Name" v-model="newModuleName" required></v-text-field>
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
  import { IDepartmentUpdate } from '@/interfaces';
  import {  dispatchUpdateDepartment, dispatchGetModuleNames } from '@/store/admin/actions';
  import { readAdminOneDepartment, readModuleNames } from '@/store/admin/getters';

  @Component
  export default class EditDepartment extends Vue {
    public valid = false;
    public name: string = '';
    public moduleName: string = '';
    public options: any = [];
    public addNewModule: boolean = false;
    public newModuleName: string = '';
    private id: number = -1;
    private departmentId: number = -1;

    public async mounted() {
      await dispatchGetModuleNames(this.$store);
      this.options = this.moduleNames?.modules;
      this.options.push('+ Add New');
      this.id = parseInt(this.$router.currentRoute.params.id, 10);
      this.departmentId = parseInt(this.$router.currentRoute.params.departmentId, 10);
      this.setData(this.department);
      this.reset();
    }

    public reset() {
      this.name = '';
      this.$validator.reset();
      if (this.department) {
        this.setData(this.department);
      }
    }

    public onModuleChange(select) {
      if (select === '+ Add New') {
        this.addNewModule = true;
      }
    }

    public setData(department) {
      this.name = department?.name;
      this.moduleName = department?.module_name;
    }

    public cancel() {
      this.$router.back();
    }

    public async submit() {
      if (await this.$validator.validateAll()) {
        const updatedDepartment: IDepartmentUpdate = {
          id: this.departmentId,
          name: this.name,
          module_name: this.newModuleName || this.moduleName,
        };
        await dispatchUpdateDepartment(this.$store, {id: this.departmentId, department: updatedDepartment});
        this.$router.push('/main/admin/lab/' + this.id);
      }
    }

    get department() {
      return readAdminOneDepartment(this.$store)(+this.departmentId);
    }

    get moduleNames() {
      return readModuleNames(this.$store);
    }
  }
</script>
