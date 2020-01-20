<template>

    <div class="process">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-cascades"></i> Process</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-table :data="value" border class="table" ref="multipleTable">
                <el-table-column prop="test_run_id" label="TestRunId" width="260" show-overflow-tooltip></el-table-column>
                <el-table-column prop="mapa_restarted_success" label="MAPA拉起" width="100" show-overflow-tooltip></el-table-column>
                <el-table-column prop="created_time" label="日期" width="160" sortable show-overflow-tooltip></el-table-column>
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
                var api = 'http://10.1.1.76:9999/api/v1/commits/builds/tests/process?test_run_id=' + this.test_run_id + '&page=' + this.cur_page;
                Axios.get(api, {}).then(res => {
                    this.value = res.data.value;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
        },
        mounted() {
            this.test_run_id = this.$route.query.test_run_id;
            var api = 'http://10.1.1.76:9999/api/v1/commits/builds/tests/process?test_run_id=' + this.test_run_id;
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
