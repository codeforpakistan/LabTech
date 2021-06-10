import { Component, Vue } from 'vue-property-decorator';
<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Indicators
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" :to="'/main/admin/hospital/' + id + '/department/create'">Create Indicator</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="departments">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.module_name }}</td>
        <td class="justify-center layout px-0" colspan="2">
          <v-tooltip top>
            <span>View/Add/Edit Survey</span>
            <v-btn slot="activator" flat :to="{path: `/main/admin/hospital/${id}/department/${props.item.id}`, params: {departmentId: props.item.id}}">
              <v-icon>home</v-icon>
            </v-btn>
          </v-tooltip>
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{path: `/main/admin/hospital/${id}/department/edit/${props.item.id}`, params: {departmentId: props.item.id}}">
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
import { readHospitalDepartments } from '@/store/admin/getters';
import { dispatchGetHospitalDepartments } from '@/store/admin/actions';


@Component
export default class AdminHospitals extends Vue {
  [x: string]: any;
  public id: any;
  public headers = [
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left',
    },
    {
      text: 'Module Name',
      sortable: true,
      value: 'name',
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
    await dispatchGetHospitalDepartments(this.$store, this.id);
  }

  get departments() {
    return readHospitalDepartments(this.$store);
  }
}
</script>
