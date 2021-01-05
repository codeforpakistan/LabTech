import { Component, Vue } from 'vue-property-decorator';
<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Survey
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/hospital/1/department/1/survey/create">Create Survey</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="departmentSurveys">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.questions | json }}</td>
        <td class="justify-center layout px-0" colspan="2">
          <v-tooltip top>
            <span>View / Edit Departments</span>
            <v-btn slot="activator" flat :to="{name: 'main-admin-hospitals-departments-survey', params: {id: props.item.id}}">
              <v-icon>home</v-icon>
            </v-btn>
          </v-tooltip>
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-admin-users-edit', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readDepartmentSurveys } from '@/store/admin/getters';
import { dispatchGetDepartmentSurveys } from '@/store/admin/actions';
import { ISurvey } from '@/interfaces';


@Component
export default class AdminHospitals extends Vue {
  [x: string]: any;
  public id: any;
  public hospitals: ISurvey[] = [];
  public headers = [
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left',
    },
    {
      text: 'Questions',
      sortable: false,
      value: 'questions',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
      colspan: 2,
      align: 'center',
    },
  ];

  public async mounted() {
    this.id = this.$router.currentRoute.params.id;
    await dispatchGetDepartmentSurveys(this.$store, this.id);
  }

  get departmentSurveys() {
    return readDepartmentSurveys(this.$store);
  }
}
</script>
