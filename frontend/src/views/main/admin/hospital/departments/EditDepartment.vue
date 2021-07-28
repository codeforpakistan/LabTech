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
            <v-text-field label="Module Name" v-model="moduleName" required></v-text-field>
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
  import { IDepartmentUpdate } from '@/interfaces';
  import { dispatchGetHospitalDepartments, dispatchUpdateDepartment } from '@/store/admin/actions';
  import { readAdminOneDepartment } from '@/store/admin/getters';

  @Component
  export default class EditDepartment extends Vue {
    public valid = false;
    public name: string = '';
    public moduleName: string = '';
    private id: number = -1;
    private departmentId: number = -1;

    public async mounted() {
      this.id = parseInt(this.$router.currentRoute.params.id, 10);
      this.departmentId = parseInt(this.$router.currentRoute.params.departmentId, 10);
      await dispatchGetHospitalDepartments(this.$store, this.id);
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

    public setData(department) {
      this.name = department?.name;
      this.moduleName = department?.moduleName;
    }

    public cancel() {
      this.$router.back();
    }

    public async submit() {
      if (await this.$validator.validateAll()) {
        const updatedDepartment: IDepartmentUpdate = {
          id: this.departmentId,
          name: this.name,
          module_name: this.moduleName,
        };
        await dispatchUpdateDepartment(this.$store, {id: this.departmentId, department: updatedDepartment});
        this.$router.push('/main/admin/lab/' + this.id);
      }
    }

    get department() {
      return readAdminOneDepartment(this.$store)(+this.departmentId);
    }
  }
</script>
