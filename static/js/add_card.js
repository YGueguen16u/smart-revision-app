let tagsData = new Map(); // Structure pour stocker les tags et sous-tags

function createSubTagInput(parentTagId, level = 1) {
    if (level > 8) return null;
    
    const container = document.createElement('div');
    container.className = 'subtag-input-group ms-4 mt-2';
    container.style.display = 'block';
    
    const inputGroup = document.createElement('div');
    inputGroup.className = 'd-flex gap-2';
    
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'form-control subtag-input';
    input.placeholder = 'Nouveau sous-tag';
    
    const addBtn = document.createElement('button');
    addBtn.type = 'button';
    addBtn.className = 'btn btn-secondary add-subtag-btn';
    addBtn.textContent = 'Ajouter Sous-tag';
    
    inputGroup.appendChild(input);
    inputGroup.appendChild(addBtn);
    container.appendChild(inputGroup);
    
    const subTagsList = document.createElement('div');
    subTagsList.className = 'subtags-list mt-2';
    container.appendChild(subTagsList);
    
    addBtn.addEventListener('click', () => {
        const subTagValue = input.value.trim();
        if (!subTagValue) return;
        
        let parentTag = tagsData.get(parentTagId);
        if (!parentTag) {
            // Chercher dans les sous-tags
            for (let tag of tagsData.values()) {
                parentTag = findTagById(tag, parentTagId);
                if (parentTag) break;
            }
        }
        
        if (!parentTag) return;
        
        if (!parentTag.subtags) {
            parentTag.subtags = [];
        }
        
        if (parentTag.subtags.length >= 20) {
            alert('Maximum 20 sous-tags par tag');
            return;
        }
        
        const subTagId = `${parentTagId}_${Date.now()}`;
        const subTagData = { 
            id: subTagId, 
            name: subTagValue,
            subtags: []
        };
        
        parentTag.subtags.push(subTagData);
        
        const subTagElement = createTagElement(subTagValue, subTagId, level);
        subTagsList.appendChild(subTagElement);
        input.value = '';
    });
    
    return container;
}

function findTagById(tag, id) {
    if (tag.id === id) return tag;
    if (tag.subtags) {
        for (let subtag of tag.subtags) {
            const found = findTagById(subtag, id);
            if (found) return found;
        }
    }
    return null;
}

function createTagElement(tagName, tagId, level = 1) {
    const tagDiv = document.createElement('div');
    tagDiv.className = 'tag-item mt-2 p-2 border rounded';
    
    const tagContent = document.createElement('div');
    tagContent.className = 'd-flex align-items-center gap-2';
    
    const tagText = document.createElement('span');
    tagText.textContent = tagName;
    tagText.className = 'flex-grow-1';
    
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.className = 'btn btn-sm btn-danger';
    deleteBtn.textContent = '×';
    
    tagContent.appendChild(tagText);
    tagContent.appendChild(deleteBtn);
    tagDiv.appendChild(tagContent);
    
    if (level < 8) {
        const subTagContainer = createSubTagInput(tagId, level + 1);
        tagDiv.appendChild(subTagContainer);
    }
    
    deleteBtn.addEventListener('click', () => {
        // Supprimer le tag et tous ses sous-tags
        let parentTag = null;
        let tagToDelete = null;
        
        for (let tag of tagsData.values()) {
            if (tag.id === tagId) {
                tagsData.delete(tagId);
                tagToDelete = tag;
                break;
            }
            const result = findAndRemoveTag(tag, tagId);
            if (result) {
                parentTag = tag;
                tagToDelete = result;
                break;
            }
        }
        
        tagDiv.remove();
    });
    
    return tagDiv;
}

function findAndRemoveTag(parentTag, tagId) {
    if (!parentTag.subtags) return null;
    
    const index = parentTag.subtags.findIndex(tag => tag.id === tagId);
    if (index !== -1) {
        return parentTag.subtags.splice(index, 1)[0];
    }
    
    for (let subtag of parentTag.subtags) {
        const result = findAndRemoveTag(subtag, tagId);
        if (result) return result;
    }
    
    return null;
}

document.addEventListener('DOMContentLoaded', function() {
    const addTagBtn = document.querySelector('.add-tag-btn');
    if (!addTagBtn) return;

    addTagBtn.addEventListener('click', () => {
        const input = document.querySelector('.tag-input');
        const tagValue = input.value.trim();
        if (!tagValue) return;
        
        if (tagsData.size >= 20) {
            alert('Maximum 20 tags principaux');
            return;
        }
        
        const tagId = `tag_${Date.now()}`;
        const tagData = {
            id: tagId,
            name: tagValue,
            subtags: []
        };
        
        tagsData.set(tagId, tagData);
        
        const tagElement = createTagElement(tagValue, tagId);
        document.getElementById('tagsList').appendChild(tagElement);
        input.value = '';
    });

    document.getElementById('cardForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const currentDate = new Date().toISOString().split('T')[0];
        
        function convertTagsToJson(tag) {
            const result = { name: tag.name };
            if (tag.subtags && tag.subtags.length > 0) {
                result.subtags = tag.subtags.map(convertTagsToJson);
            }
            return result;
        }
        
        const cardData = {
            type: "traditional",
            question: document.getElementById('question').value,
            response: document.getElementById('response').value,
            tags: Array.from(tagsData.values()).map(convertTagsToJson),
            feedback: document.getElementById('feedback').value,
            date_created: currentDate,
            date_last_reviewed: currentDate,
            date_next_review: currentDate,
            statistics: {
                successes: 0,
                failures: 0
            },
            multimedia: {
                image: null,
                audio: null,
                video: null
            }
        };

        fetch(`/api/decks/${deckName}/cards`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cardData)
        })
        .then(response => {
            if (response.ok) {
                window.location.href = `/decks/${deckName}`;
            } else {
                alert('Erreur lors de l\'ajout de la carte');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Erreur lors de l\'ajout de la carte');
        });
    });
});
