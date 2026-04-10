<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';

const addTag = () => {
    console.log("登録成功")
}
</script>

<template>
    <h1>タグ新規追加</h1>
    <div class="form-group">
        <input v-model="newTagTitle" placeholder="新しいタグ名" />
        <button class="btn-submit" @click="addTag">登録</button>
    </div>
    <router-link to="/tags" class="btn-back">← 戻る</router-link>
</template>