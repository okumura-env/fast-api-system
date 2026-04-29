<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';
import { useRouter, useRoute  } from "vue-router";

const router = useRouter();
const route = useRoute();
const tagId = ref(route.params.id);
const isEditMode = ref(!!route.params.id);

const newTagTitle = ref("");
const onSubmit = async() => {
    const formData = {
        title: newTagTitle.value,
    }

    if(isEditMode.value){
        await client.put(`/tags/${tagId.value}`,formData);
    }else{
        await client.post('/tags',formData);
    }
    
    router.push('/tags');
}

onMounted(async () => {
    if(isEditMode.value==true){
        const response = await client.get(`/tags/${tagId.value}`);
        newTagTitle.value = response.data.title;
    }
})
</script>

<template>
    <h1>{{ isEditMode ? "タグ編集" : "タグ新規追加" }}</h1>
    <div class="form-group">
        <input v-model="newTagTitle" placeholder="新しいタグ名" />
        <button class="btn-submit" @click="onSubmit">{{ isEditMode ? "更新" : "登録" }}</button>
    </div>
    <router-link to="/tags" class="btn-back">← 戻る</router-link>
</template>