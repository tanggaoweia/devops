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
                <el-table-column prop="scene_type" label="场景" width="150" show-overflow-tooltip></el-table-column>
                <el-table-column prop="precision_rt" label="准确率" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="recall_rt" label="召回率" width="100" show-overflow-tooltip></el-table-column>
                <el-table-column prop="manual_count" label="真值车框数目" width="100" show-overflow-tooltip></el-table-column>
                <el-table-column prop="algorithm_count" label="算法车框数目" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="overlapping_count" label="合格车框数目" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="created_time" label="日期" sortable width="160"></el-table-column>
            </el-table>
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

        mounted() {
            this.test_run_id = this.$route.query.test_run_id;
            var api = 'http://10.1.1.76:9999/api/v1/commits/builds/tests/software?test_run_id=' + this.test_run_id;
            Axios.get(api, {}).then(res => {
                this.value = res.data.value;
                console.log(this.value)

            }).catch(error => {
                console.log('Error', error.message)
            });
        },
    }
</script>

<style scoped>
</style>
