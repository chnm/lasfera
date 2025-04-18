// The following script handles the admin and back-end work for the text annotations.
document.addEventListener("DOMContentLoaded", function() {
    // First add the styles to document head in admin view
    addStyles();
    
    // Initialize the annotation system only after Trix is ready
    if (typeof Trix !== 'undefined') {
        initializeAnnotationSystem();
    } else {
        console.error('Trix editor not found. Make sure trix.js is loaded.');
    }
});

function addStyles() {
    const modalStyle = document.createElement("style");
    modalStyle.textContent = `
        .annotation-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        }
        
        .annotation-modal-content {
            background: white;
            padding: 20px;
            border-radius: 8px;
            width: 400px;
            max-width: 90%;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .annotation-modal h3 {
            margin: 0 0 15px 0;
            font-size: 18px;
        }
        
        .annotation-modal textarea {
            width: 100%;
            min-height: 100px;
            margin: 10px 0;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
        }
        
        .annotation-modal select {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        .annotation-modal-buttons {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 15px;
        }
        
        .annotation-modal button {
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            border: none;
            font-size: 14px;
        }
        
        .annotation-modal .btn-save {
            background: #007bff;
            color: white;
        }
        
        .annotation-modal .btn-cancel {
            background: #6c757d;
            color: white;
        }
        
        .selected-text-preview {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
            border: 1px solid #dee2e6;
        }
    `;
    document.head.appendChild(modalStyle);
}

function initializeAnnotationSystem() {
    // Wait for Trix editor to be initialized
    document.addEventListener('trix-initialize', function() {
        const toolbar = document.querySelector('trix-toolbar .trix-button-row');
        if (!toolbar) {
            console.error('Trix toolbar not found');
            return;
        }

        // Check if we've already added the button
        if (toolbar.querySelector('.trix-button--icon-note')) {
            return;
        }

        addAnnotationButton(toolbar);
    });

    // Initialize existing annotations
    loadExistingAnnotations();
}

function addAnnotationButton(toolbar) {
    const annotationGroup = document.createElement('span');
    annotationGroup.className = 'trix-button-group';
    annotationGroup.setAttribute('data-trix-button-group', 'annotation-tools');
    
    const annotateButton = document.createElement('button');
    annotateButton.type = 'button';
    annotateButton.className = 'trix-button trix-button--icon trix-button--icon-note';
    annotateButton.setAttribute('data-trix-action', 'addAnnotation');
    annotateButton.title = 'Add Note';
    
    // Add note icon styles
    if (!document.querySelector('#annotation-styles')) {
        const iconStyle = document.createElement('style');
        iconStyle.id = 'annotation-styles';
        iconStyle.textContent = `
            .trix-button--icon-note::before {
                background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>');
            }
        `;
        document.head.appendChild(iconStyle);
    }
    
    annotationGroup.appendChild(annotateButton);
    toolbar.appendChild(annotationGroup);
    
    // Add click handler
    annotateButton.addEventListener('click', handleAnnotationClick);
}

function getStanzaId() {
    const urlMatch = window.location.pathname.match(/\/(stanza|stanzatranslated)\/(\d+)/);
    if (urlMatch) return urlMatch[2];

    const form = document.querySelector("#stanza_form, #stanzatranslated_form");
    if (form) {
        const objectId = form.getAttribute("data-object-id") || 
                        form.querySelector('input[name="object_id"]')?.value;
        if (objectId) return objectId;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const objectId = urlParams.get("object_id");
    if (objectId) return objectId;

    const breadcrumbs = document.querySelector(".breadcrumbs");
    if (breadcrumbs) {
        const match = breadcrumbs.textContent.match(/Stanza\s+(\d+)/);
        if (match) return match[1];
    }

    const hiddenId = document.querySelector('input[name="stanza_id"], input[name="id"]')?.value;
    if (hiddenId) return hiddenId;

    console.error("Could not find stanza ID. URL:", window.location.href);
    return null;
}

function handleAnnotationClick(event) {
    event.preventDefault();

    const editor = document.querySelector("trix-editor").editor;
    const selectedRange = editor.getSelectedRange();

    if (selectedRange[0] === selectedRange[1]) {
        alert("Please select some text to annotate");
        return;
    }

    const selectedText = editor.getDocument().getStringAtRange(selectedRange);
    const stanzaId = getStanzaId();

    if (!stanzaId) {
        alert("Could not determine which stanza to annotate");
        return;
    }

    // Create and append modal
    const modal = document.createElement("div");
    modal.className = "annotation-modal";
    modal.innerHTML = `
        <div class="annotation-modal-content">
            <h3>Add Annotation</h3>
            <div class="selected-text-preview">
                Selected text: <strong>${selectedText}</strong>
            </div>
            <textarea id="annotation-text" 
                placeholder="Enter your annotation..."
                autofocus></textarea>
            <select id="annotation-type">
                <option value="note">Editorial Note</option>
                <option value="translation">Translation</option>
                <option value="variant">Textual Variant</option>
                <option value="reference">Cross Reference</option>
            </select>
            <div class="annotation-modal-buttons">
                <button type="button" class="btn-cancel">Cancel</button>
                <button type="button" class="btn-save">Save</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Focus the textarea
    setTimeout(() => {
        const textarea = modal.querySelector("#annotation-text");
        if (textarea) {
            textarea.focus();
        }
    }, 100);

    // Handle modal buttons
    modal.querySelector(".btn-cancel").addEventListener("click", () => {
        modal.remove();
    });

    modal.querySelector(".btn-save").addEventListener("click", () => {
        const annotationText = modal.querySelector("#annotation-text").value;
        const annotationType = modal.querySelector("#annotation-type").value;

        if (!annotationText.trim()) {
            alert("Please enter an annotation");
            return;
        }

        // Get CSRF token
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
        if (!csrfToken) {
            console.error("No CSRF token found");
            alert("Security token missing");
            return;
        }

        // Prepare the data
        const formData = new FormData();
        formData.append("model_type", 
            window.location.pathname.includes("stanzatranslated") ? "stanzatranslated" : "stanza"
        );
        formData.append("stanza_id", stanzaId);
        formData.append("selected_text", selectedText);
        formData.append("annotation", annotationText);
        formData.append("annotation_type", annotationType);
        formData.append("from_pos", selectedRange[0]);
        formData.append("to_pos", selectedRange[1]);
        formData.append("csrfmiddlewaretoken", csrfToken);

        // Add loading state to save button
        const saveButton = modal.querySelector(".btn-save");
        const originalButtonText = saveButton.textContent;
        saveButton.textContent = "Saving...";
        saveButton.disabled = true;

        fetch("/text-annotations/create/", {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            credentials: "same-origin", // Important for CSRF
        })
        .then(response => {
            return response.json().then(data => ({ status: response.status, data }));
        })
        .then(({ status, data }) => {
            if (status === 200 && data.success) {
                // Create the annotated span with proper attributes and styling
                editor.setSelectedRange(selectedRange);
                const annotatedSpan = `
                    <span 
                        class="annotated-text" 
                        data-annotation-id="${data.annotation_id}" 
                        data-annotation="${annotationText}"
                        data-annotation-type="${annotationType}"
                    >${selectedText}</span>
                `;
                editor.insertHTML(annotatedSpan);

                // Close the modal
                modal.remove();

                // Show success message
                const successMessage = document.createElement("div");
                successMessage.className = "annotation-success-message";
                successMessage.textContent = "Annotation saved successfully";
                successMessage.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #28a745;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 4px;
                    z-index: 10000;
                `;
                document.body.appendChild(successMessage);
                setTimeout(() => successMessage.remove(), 3000);

                // Add hover listener for the newly created annotation
                const newAnnotation = editor.element.querySelector(
                    `[data-annotation-id="${data.annotation_id}"]`
                );
                if (newAnnotation) {
                    addAnnotationHoverListener(newAnnotation, annotationType, annotationText);
                }
            } else {
                throw new Error(data.error || "Failed to save annotation");
            }
        })
        .catch(error => {
            console.error("Error saving annotation:", error);
            saveButton.textContent = originalButtonText;
            saveButton.disabled = false;
            alert("Failed to save annotation. Please try again.");
        });
    });
}

function addAnnotationHoverListener(element, type, text) {
    element.addEventListener("mouseenter", function(e) {
        const tooltip = document.createElement("div");
        tooltip.className = "annotation-tooltip";
        tooltip.innerHTML = `
            <strong>${type}:</strong><br>
            ${text}
        `;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
            z-index: 1000;
            max-width: 300px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        `;

        const rect = element.getBoundingClientRect();
        tooltip.style.left = `${rect.left}px`;
        tooltip.style.top = `${rect.top - tooltip.offsetHeight - 8}px`;

        document.body.appendChild(tooltip);

        element.addEventListener("mouseleave", function() {
            tooltip.remove();
        }, { once: true });
    });
}

function loadExistingAnnotations() {
    const stanzaId = getStanzaId();
    if (!stanzaId) return;

    fetch(`/text-annotations/get/${stanzaId}/`)
        .then(response => response.json())
        .then(annotations => {
            annotations.forEach(annotation => {
                // Find the text node containing this annotation
                const editor = document.querySelector("trix-editor").editor;
                const content = editor.getDocument().toString();
                const index = content.indexOf(annotation.selected_text);

                if (index !== -1) {
                    const range = [index, index + annotation.selected_text.length];
                    editor.setSelectedRange(range);
                    const annotatedSpan = `
                        <span 
                            class="annotated-text" 
                            data-annotation-id="${annotation.id}" 
                            data-annotation="${annotation.annotation}"
                            data-annotation-type="${annotation.annotation_type}"
                        >${annotation.selected_text}</span>
                    `;
                    editor.insertHTML(annotatedSpan);
                }
            });
        })
        .catch(error => console.error("Error loading annotations:", error));
}
