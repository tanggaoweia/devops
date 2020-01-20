<template>

    <div class="tests">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-cascades"></i> Tests</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-table :data="value" border class="table" ref="multipleTable">
                <el-table-column prop="test_run_id" label="TestRunId" width="250" show-overflow-tooltip></el-table-column>
                <el-table-column prop="uuid" label="UUID" width="230" show-overflow-tooltip></el-table-column>
                <el-table-column prop="android_version" label="安卓版本" width="100" show-overflow-tooltip></el-table-column>
                <el-table-column prop="app_version" label="APP版本" width="100" show-overflow-tooltip></el-table-column>
                <el-table-column prop="source" label="来源" width="100" show-overflow-tooltip></el-table-column>
                <el-table-column prop="process_total_num" label="进程测试总次数" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="process_pass_num" label="进程测试通过次数" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="hardware_total_num" label="硬件测试总次数" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="hardware_pass_num" label="硬件测试通过次数" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="created_time" label="日期" width="135" sortable show-overflow-tooltip></el-table-column>
                <el-table-column label="操作"  align="center" width="175" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <el-button type="text" icon="el-icon-view" @click="handleProcess(scope.row)">进程</el-button>
                        <el-button type="text" icon="el-icon-view" @click="handleHardware(scope.row)">硬件</el-button>
                        <el-button type="text" icon="el-icon-view" @click="handleWardware(scope.row)">软件</el-button>
                    </template>
                </el-table-column>
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
                build_id: '',
            }
        },
        methods: {
            // 分页导航
            handleCurrentChange(val) {
                this.cur_page = val;
                this.getData();

            },
            handleProcess(row) {
                this.$router.push({path:'/process', query:{test_run_id: row['test_run_id']}})
            },
           handleHardware(row) {
                this.$router.push({path:'/hardware', query:{test_run_id: row['test_run_id']}})
            },
            handleWardware(row) {
                this.$router.push({path:'/software', query:{test_run_id: row['test_run_id']}})
            },
            getData() {
                var api = 'http://10.1.1.76:9999/api/v1/commits/builds/tests?build_id=' + this.build_id + '&page=' + this.cur_page;
                Axios.get(api, {}).then(res => {
                    this.value = res.data.value;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
        },
        mounted() {
            this.build_id = this.$route.query.build_id;
            var api = 'http://10.1.1.76:9999/api/v1/commits/builds/tests?build_id=' + this.build_id;
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
