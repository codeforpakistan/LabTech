import { Component, Vue } from 'vue-property-decorator';
<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Hospital
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/hospital/create">Create Hospital</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="hospitals">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.address }}</td>
        <td>{{ props.item.created_date }}</td>
        <td>{{ props.item.lat }}</td>
        <td>{{ props.item.lng }}</td>
        <td class="justify-center layout px-0" colspan="2">
          <v-tooltip top>
            <span>View / Edit Departments</span>
            <v-btn slot="activator" flat :to="{name: 'main-admin-hospitals-departments', params: {id: props.item.id}}">
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
import { readAdminHospital } from '@/store/admin/getters';
import { dispatchGetHospitals } from '@/store/admin/actions';
import { IHospital } from '@/interfaces';


@Component
export default class AdminHospitals extends Vue {
  [x: string]: any;
  public headers = [
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left',
    },
    {
      text: 'Address',
      sortable: true,
      value: 'address',
      align: 'left',
    },
    {
      text: 'Created Date',
      sortable: true,
      value: 'create_date',
      align: 'left',
    },
    {
      text: 'Lattitue',
      sortable: true,
      value: 'lat',
      align: 'left',
    },
    {
      text: 'Longitude',
      sortable: true,
      value: 'lng',
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
    await dispatchGetHospitals(this.$store);
  }

  get hospitals() {
    return readAdminHospital(this.$store);
  }
}
</script>
