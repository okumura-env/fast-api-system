<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const ingredientId = ref(route.params.id);
const isEditMode = ref(!!route.params.id);

const newIngredientName = ref("");

const onSubmit = async() => {
    const formData = {
        name: newIngredientName.value,
    }

    if(isEditMode.value){
        await client.put(`/ingredients/${ingredientId.value}`, formData);
    }else{
        await client.post('/ingredients', formData);
    }

    router.push('/ingredients');
}

onMounted(async () => {
    if(isEditMode.value == true){
        const response = await client.get(`/ingredients/${ingredientId.value}`);
        newIngredientName.value = response.data.name;
    }
})
</script>

<template>
    <h1>{{ isEditMode ? "食材編集" : "食材新規追加" }}</h1>
    <div class="form-group">
        <input v-model="newIngredientName" placeholder="新しい食材名" />
        <button class="btn-submit" @click="onSubmit">{{ isEditMode ? "更新" : "登録" }}</button>
    </div>
    <router-link to="/ingredients" class="btn-back">← 戻る</router-link>
</template>
