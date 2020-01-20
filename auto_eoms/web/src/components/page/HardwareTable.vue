<template>

    <div class="tests">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-cascades"></i> Hardware</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-table :data="value" border class="table" ref="multipleTable">
                <el-table-column prop="test_run_id" label="TestRunId" width="250" show-overflow-tooltip></el-table-column>
                <el-table-column prop="airplan_off_to_on" label="飞行模式从关到开" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="airplan_on_to_off" label="飞行模式从开到关" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="mobile4g_off_to_on" label="4G从关到开" width="100" show-overflow-tooltip></el-table-column>
                <el-table-column prop="mobile4g_on_to_off" label="4G从开到关" width="100" show-overflow-tooltip></el-table-column>
                <el-table-column prop="gps_status" label="GPS状态" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="acc_status" label="ACC状态" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="sdcard_status" label="SD卡状态" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="wifi_status" label="WIFI状态" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="has_restarted" label="重启" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="cpu_temp" label="CPU温度" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="created_time" label="日期" sortable width="160"></el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination background @current-change="handleCurrentChange" layout="prev, pager, next"
                               :total="total">
                </el-pagination>
            </div>
        </div>
    </div>
</template>

<script>
    import Axios from 'axios'

    export default {
        name: 'BaseTable',
        data() {
            return {
                total: 0,
                value: [],
                test_run_id: '',
            }
        },
        methods: {
            // 分页导航
            handleCurrentChange(val) {
                this.cur_page = val;
                this.getData();

            },
            getData() {
                var api = 'http://10.1.1.76:9999/api/v1/commits/builds/tests/hardware?test_run_id=' + this.test_run_id + '&page=' + this.cur_page;
                Axios.get(api, {}).then(res => {
                    this.value = res.data.value;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
        },
        mounted() {
            this.test_run_id = this.$route.query.test_run_id;
            var api = 'http://10.1.1.76:9999/api/v1/commits/builds/tests/hardware?test_run_id=' + this.test_run_id;
            Axios.get(api, {}).then(res => {
                this.value = res.data.value;
                this.total = res.data.total_num;

            }).catch(error => {
                console.log('Error', error.message)
            });
        },
    }
</script>

<style scoped>
</style>
