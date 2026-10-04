const API_BASE = "http://127.0.0.1:8000";

let currentTemplate = null;
let productImageData = null;
let referenceImageData = null;

let creativeSettings = {
    headline: "",
    description: "",
    callToAction: "",
    background: "#172033",
    accent: "#60A5FA",
    foreground: "#FFFFFF"
};

document.addEventListener("DOMContentLoaded", () => {
    initializeCampaignGenerator();
    initializeCreativeStudio();
    initializeTemplateGenerator();
});

// =====================================
// CAMPAIGN GENERATOR
// =====================================

function initializeCampaignGenerator() {
    const button = document.getElementById("generateButton");
    if (!button) return;

    button.addEventListener("click", async () => {
        const product = document.getElementById("productName")?.value.trim();
        const audience = document.getElementById("targetAudience")?.value.trim();
        const goal = document.getElementById("marketingGoal")?.value.trim();
        const budget = Number(document.getElementById("campaignBudget")?.value || 0);

        const message = document.getElementById("campaignMessage");
        const results = document.getElementById("campaignResults");
        const output = document.getElementById("campaignOutput");

        if (!product || !audience || !goal) {
            if (message) message.textContent = "Please complete all required fields.";
            return;
        }

        button.disabled = true;
        button.textContent = "Generating Campaign...";

        if (message) message.textContent = "Analyzing your campaign...";
        if (results) results.classList.add("hidden");

        try {
            const response = await fetch(`${API_BASE}/generate-campaign`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    product_name: product,
                    target_audience: audience,
                    marketing_goal: goal,
                    budget
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Campaign generation failed");
            }

            if (output) {
                output.textContent = JSON.stringify(data, null, 2);
            }

            if (results) results.classList.remove("hidden");

            if (message) {
                message.textContent = "Campaign generated successfully.";
            }

        } catch (error) {
            if (message) {
                message.textContent =
                    error.message || "Could not connect to RIVAAN backend.";
            }

        } finally {
            button.disabled = false;
            button.textContent = "Generate Campaign";
        }
    });
}

// =====================================
// CREATIVE STUDIO CONTROLS
// =====================================

function initializeCreativeStudio() {
    const formPanel = document.querySelector(
        "#templatePage .template-studio .studio-panel"
    );

    if (!formPanel || document.getElementById("creativeEditorFields")) {
        return;
    }

    const editor = document.createElement("div");
    editor.id = "creativeEditorFields";

    editor.innerHTML = `
        <div style="border-top:1px solid var(--border-color,#293247);margin:22px 0;padding-top:20px;">
            <h3>Images</h3>

            <div class="studio-field">
                <label for="productImageInput">Your Product Image</label>
                <input
                    id="productImageInput"
                    type="file"
                    accept="image/png,image/jpeg,image/webp"
                >
                <small class="studio-message">
                    Choose a clear product photo. It stays in this browser session.
                </small>
            </div>

            <div class="studio-field">
                <label for="referenceImageInput">
                    Reference Design (optional)
                </label>
                <input
                    id="referenceImageInput"
                    type="file"
                    accept="image/png,image/jpeg,image/webp"
                >
                <small class="studio-message">
                    Reference is shown for guidance; this version does not
                    automatically recreate its design.
                </small>
            </div>

            <div
                id="imageUploadMessage"
                class="studio-message"
                aria-live="polite"
            ></div>
        </div>

        <div style="border-top:1px solid var(--border-color,#293247);margin:22px 0;padding-top:20px;">
            <h3>Live Editing</h3>

            <div class="studio-field">
                <label for="editHeadline">Headline</label>
                <input
                    id="editHeadline"
                    type="text"
                    maxlength="90"
                    placeholder="Your campaign headline"
                >
            </div>

            <div class="studio-field">
                <label for="editDescription">Short Description</label>
                <textarea
                    id="editDescription"
                    maxlength="240"
                    placeholder="A short product benefit"
                ></textarea>
            </div>

            <div class="studio-field">
                <label for="editCTA">Call to Action</label>
                <input
                    id="editCTA"
                    type="text"
                    maxlength="32"
                    placeholder="Shop Now"
                >
            </div>

            <div class="studio-field">
                <label for="editBackground">Background Color</label>
                <input
                    id="editBackground"
                    type="color"
                    value="#172033"
                    style="height:48px;padding:5px;"
                >
            </div>

            <div class="studio-field">
                <label for="editAccent">Accent / Button Color</label>
                <input
                    id="editAccent"
                    type="color"
                    value="#60A5FA"
                    style="height:48px;padding:5px;"
                >
            </div>

            <div class="studio-field">
                <label for="editForeground">Text Color</label>
                <input
                    id="editForeground"
                    type="color"
                    value="#FFFFFF"
                    style="height:48px;padding:5px;"
                >
            </div>

            <button type="button" id="resetCreativeButton">
                Reset editor fields
            </button>
        </div>
    `;

    formPanel.appendChild(editor);

    const productInput = document.getElementById("productImageInput");
    const referenceInput = document.getElementById("referenceImageInput");

    productInput.addEventListener("change", event => {
        readImageFile(event.target.files?.[0], "product");
    });

    referenceInput.addEventListener("change", event => {
        readImageFile(event.target.files?.[0], "reference");
    });

    [
        "editHeadline",
        "editDescription",
        "editCTA",
        "editBackground",
        "editAccent",
        "editForeground"
    ].forEach(id => {
        document.getElementById(id).addEventListener("input", () => {
            syncEditorSettings();
            updateCreativePreview();
        });
    });

    document.getElementById("resetCreativeButton").addEventListener("click", () => {
        const template = currentTemplate || {};

        setEditorValues({
            headline: template.headline || "",
            description: template.description || "",
            callToAction: template.call_to_action || "",
            background: (template.color_palette || [])[0] || "#172033",
            accent: (template.color_palette || [])[1] || "#60A5FA",
            foreground: (template.color_palette || [])[2] || "#FFFFFF"
        });

        updateCreativePreview();
    });
}

function readImageFile(file, kind) {
    const message = document.getElementById("imageUploadMessage");

    if (!file) return;

    if (!["image/png", "image/jpeg", "image/webp"].includes(file.type)) {
        if (message) {
            message.textContent = "Please select a PNG, JPG, or WebP image.";
        }
        return;
    }

    const maxBytes = 8 * 1024 * 1024;

    if (file.size > maxBytes) {
        if (message) {
            message.textContent = "Please choose an image smaller than 8 MB.";
        }
        return;
    }

    const reader = new FileReader();

    reader.onload = () => {
        if (kind === "product") {
            productImageData = reader.result;
        } else {
            referenceImageData = reader.result;
        }

        if (message) {
            message.textContent = kind === "product"
                ? "Product image loaded into the preview."
                : "Reference image loaded. It is available as a visual guide.";
        }

        updateCreativePreview();
    };

    reader.onerror = () => {
        if (message) {
            message.textContent = "Could not read that image. Try another file.";
        }
    };

    reader.readAsDataURL(file);
}
// =====================================
// EDITOR STATE
// =====================================

function syncEditorSettings() {
    creativeSettings = {
        headline: document.getElementById("editHeadline")?.value || "",
        description: document.getElementById("editDescription")?.value || "",
        callToAction: document.getElementById("editCTA")?.value || "Shop Now",
        background: document.getElementById("editBackground")?.value || "#172033",
        accent: document.getElementById("editAccent")?.value || "#60A5FA",
        foreground: document.getElementById("editForeground")?.value || "#FFFFFF"
    };
}

function setEditorValues(settings = {}) {
    const fields = {
        editHeadline: settings.headline || "",
        editDescription: settings.description || "",
        editCTA: settings.callToAction || "Shop Now",
        editBackground: settings.background || "#172033",
        editAccent: settings.accent || "#60A5FA",
        editForeground: settings.foreground || "#FFFFFF"
    };

    Object.entries(fields).forEach(([id, value]) => {
        const element = document.getElementById(id);

        if (element) {
            element.value = value;
        }
    });

    syncEditorSettings();
}

// =====================================
// LIVE CREATIVE PREVIEW
// =====================================

function updateCreativePreview() {
    const result = document.getElementById("templateResult");
    if (!result) return;

    syncEditorSettings();

    const productName =
        document.getElementById("templateProductName")?.value.trim() ||
        "Your Product";

    const headline = creativeSettings.headline || productName;
    const description =
        creativeSettings.description || "Discover something made for you.";
    const cta = creativeSettings.callToAction || "Shop Now";

    const productImage = productImageData
        ? `<img src="${productImageData}" alt="Product preview" style="width:100%;height:230px;object-fit:contain;background:rgba(255,255,255,0.08);border-radius:12px;">`
        : `<div style="height:230px;display:flex;align-items:center;justify-content:center;border:1px dashed rgba(255,255,255,0.4);border-radius:12px;color:${creativeSettings.foreground};opacity:.7;">Upload a product image</div>`;

    const referenceImage = referenceImageData
        ? `<div style="margin-top:14px;"><small style="display:block;margin-bottom:6px;opacity:.75;">REFERENCE GUIDE</small><img src="${referenceImageData}" alt="Reference design guide" style="max-width:100%;max-height:150px;object-fit:contain;border-radius:8px;"></div>`
        : "";

    result.innerHTML = `
        <div style="
            background:${creativeSettings.background};
            color:${creativeSettings.foreground};
            padding:24px;
            border-radius:16px;
            max-width:520px;
            margin:12px auto;
            font-family:Arial,sans-serif;
            box-shadow:0 12px 35px rgba(0,0,0,.18);
        ">
            <div style="
                font-size:11px;
                letter-spacing:2px;
                text-transform:uppercase;
                opacity:.75;
                margin-bottom:14px;
            ">
                RIVAAN CREATIVE STUDIO
            </div>

            <h2 style="
                font-size:30px;
                line-height:1.15;
                margin:0 0 16px;
                overflow-wrap:anywhere;
            ">
                ${escapeHTML(headline)}
            </h2>

            ${productImage}

            <p style="font-size:15px;line-height:1.6;margin:18px 0;">
                ${escapeHTML(description)}
            </p>

            <div style="
                display:inline-block;
                background:${creativeSettings.accent};
                color:#101827;
                padding:12px 22px;
                border-radius:7px;
                font-weight:700;
            ">
                ${escapeHTML(cta)}
            </div>

            ${referenceImage}
        </div>

        <div style="text-align:center;margin:16px 0;">
            <button type="button" id="downloadCreativeButton">
                Download Creative PNG
            </button>
        </div>
    `;

    result.classList.remove("hidden");
    result.style.display = "block";

    document.getElementById("downloadCreativeButton")
        ?.addEventListener("click", downloadCreative);
}

// =====================================
// TEMPLATE GENERATOR
// =====================================

function initializeTemplateGenerator() {
    const button = document.getElementById("generateTemplateButton");
    if (!button) return;

    button.addEventListener("click", generateTemplate);
}

async function generateTemplate() {
    const button = document.getElementById("generateTemplateButton");
    const message = document.getElementById("templateMessage");
    const result = document.getElementById("templateResult");
    const emptyState = document.getElementById("templateEmptyState");

    const productName =
        document.getElementById("templateProductName")?.value.trim();

    const productDescription =
        document.getElementById("templateProductDescription")?.value.trim();

    const audience =
        document.getElementById("templateAudience")?.value.trim();

    const goal =
        document.getElementById("templateGoal")?.value.trim();

    const platform =
        document.getElementById("templatePlatform")?.value;

    const style =
        document.getElementById("templateStyle")?.value;

    if (!productName || !productDescription || !audience || !goal) {
        if (message) {
            message.textContent = "Please fill in all required fields.";
        }
        return;
    }

    button.disabled = true;
    button.textContent = "Creating Template...";

    if (message) {
        message.textContent = "Preparing your creative blueprint...";
    }

    if (emptyState) {
        emptyState.classList.add("hidden");
    }

    try {
        const response = await fetch(`${API_BASE}/generate-template`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                product_name: productName,
                product_description: productDescription,
                target_audience: audience,
                marketing_goal: goal,
                platform,
                design_style: style
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Template generation failed");
        }

        const template = data.template || data;

        currentTemplate = template;

        const palette = Array.isArray(template.color_palette)
            ? template.color_palette
            : ["#172033", "#60A5FA", "#FFFFFF"];

        setEditorValues({
            headline: template.headline || productName,
            description: template.description || productDescription,
            callToAction: template.call_to_action || "Shop Now",
            background: palette[0] || "#172033",
            accent: palette[1] || "#60A5FA",
            foreground: palette[2] || "#FFFFFF"
        });

        if (result) {
            result.classList.remove("hidden");
            result.style.display = "block";
            result.innerHTML = "";
        }

        updateCreativePreview();

        if (message) {
            message.textContent =
                "Creative blueprint ready. You can now edit the preview.";
        }

    } catch (error) {
        if (message) {
            message.textContent =
                error.message || "Could not connect to backend.";
        }

        if (emptyState) {
            emptyState.classList.remove("hidden");
        }

    } finally {
        button.disabled = false;
        button.textContent = "Generate Template";
    }
}
// =====================================
// CREATIVE PNG EXPORT
// =====================================

async function downloadCreative() {
    syncEditorSettings();

    const productName =
        document.getElementById("templateProductName")?.value.trim() ||
        "RIVAAN-Creative";

    const headline =
        creativeSettings.headline || productName;

    const description =
        creativeSettings.description || "";

    const cta =
        creativeSettings.callToAction || "Shop Now";

    const canvas = document.createElement("canvas");

    canvas.width = 1080;
    canvas.height = 1080;

    const ctx = canvas.getContext("2d");

    if (!ctx) {
        alert("Your browser could not create the creative.");
        return;
    }

    // Background
    ctx.fillStyle = creativeSettings.background;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Subtle RIVAAN watermark
    ctx.fillStyle = creativeSettings.foreground;
    ctx.globalAlpha = 0.45;
    ctx.font = "bold 22px Arial";
    ctx.textAlign = "right";
    ctx.fillText("RIVAAN", 1005, 65);
    ctx.globalAlpha = 1;
    ctx.textAlign = "left";

    // Headline
    ctx.fillStyle = creativeSettings.foreground;
    ctx.font = "bold 66px Arial";

    const headlineLines = wrapCanvasText(ctx, headline, 930);

    let headlineY = 190;

    headlineLines.slice(0, 3).forEach(line => {
        ctx.fillText(line, 75, headlineY);
        headlineY += 78;
    });

    // Product image
    const imageAreaY = Math.max(350, headlineY + 20);
    const imageAreaHeight = 390;

    if (productImageData) {
        try {
            const image = await loadCanvasImage(productImageData);

            const maxWidth = 850;
            const maxHeight = imageAreaHeight;

            const scale = Math.min(
                maxWidth / image.width,
                maxHeight / image.height
            );

            const width = image.width * scale;
            const height = image.height * scale;

            const x = (canvas.width - width) / 2;
            const y = imageAreaY + (maxHeight - height) / 2;

            ctx.drawImage(image, x, y, width, height);

        } catch (error) {
            console.error("Product image could not be exported:", error);
        }

    } else {
        ctx.globalAlpha = 0.65;
        ctx.strokeStyle = creativeSettings.foreground;
        ctx.setLineDash([12, 10]);
        ctx.lineWidth = 3;

        ctx.strokeRect(115, imageAreaY, 850, imageAreaHeight);

        ctx.setLineDash([]);

        ctx.fillStyle = creativeSettings.foreground;
        ctx.font = "30px Arial";
        ctx.textAlign = "center";

        ctx.fillText(
            "Upload a product image",
            540,
            imageAreaY + imageAreaHeight / 2
        );

        ctx.textAlign = "left";
        ctx.globalAlpha = 1;
    }

    // Description
    const descriptionY = imageAreaY + imageAreaHeight + 55;

    ctx.fillStyle = creativeSettings.foreground;
    ctx.font = "30px Arial";

    const descriptionLines = wrapCanvasText(
        ctx,
        description,
        900
    );

    descriptionLines.slice(0, 2).forEach((line, index) => {
        ctx.fillText(line, 75, descriptionY + index * 42);
    });

    // CTA Button
    const buttonY = 925;
    const buttonWidth = 330;
    const buttonHeight = 75;

    ctx.fillStyle = creativeSettings.accent;

    ctx.beginPath();
    ctx.roundRect(
        75,
        buttonY,
        buttonWidth,
        buttonHeight,
        12
    );
    ctx.fill();

    ctx.fillStyle = "#101827";
    ctx.font = "bold 29px Arial";
    ctx.textAlign = "center";

    ctx.fillText(
        cta,
        75 + buttonWidth / 2,
        buttonY + 48
    );

    ctx.textAlign = "left";

    // Download
    canvas.toBlob(blob => {
        if (!blob) {
            alert("Could not export the creative. Please try again.");
            return;
        }

        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");

        link.href = url;
        link.download =
            `${sanitizeFileName(productName)}-RIVAAN.png`;

        document.body.appendChild(link);
        link.click();
        link.remove();

        setTimeout(() => URL.revokeObjectURL(url), 1000);

    }, "image/png");
}

// =====================================
// CANVAS TEXT WRAPPING
// =====================================

function wrapCanvasText(ctx, text, maxWidth) {
    const words = String(text || "").split(/\s+/);
    const lines = [];

    let currentLine = "";

    words.forEach(word => {
        if (!word) return;

        const testLine = currentLine
            ? `${currentLine} ${word}`
            : word;

        const width = ctx.measureText(testLine).width;

        if (width > maxWidth && currentLine) {
            lines.push(currentLine);
            currentLine = word;
        } else {
            currentLine = testLine;
        }
    });

    if (currentLine) {
        lines.push(currentLine);
    }

    return lines;
}

// =====================================
// IMAGE LOADER
// =====================================

function loadCanvasImage(source) {
    return new Promise((resolve, reject) => {
        const image = new Image();

        image.onload = () => resolve(image);
        image.onerror = () => reject(
            new Error("Image loading failed")
        );

        image.src = source;
    });
}

// =====================================
// HTML ESCAPING
// =====================================

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => {
        const entities = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        };

        return entities[character];
    });
}

// =====================================
// FILE NAME CLEANER
// =====================================

function sanitizeFileName(value) {
    return String(value || "RIVAAN-Creative")
        .trim()
        .replace(/[^a-z0-9-_]/gi, "-")
        .replace(/-+/g, "-")
        .replace(/^-|-$/g, "")
        .slice(0, 60) || "RIVAAN-Creative";
}

// =====================================
// BACKEND CONNECTION CHECK
// =====================================

async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE}/health`);

        if (!response.ok) {
            throw new Error("Backend health check failed");
        }

        const data = await response.json();

        console.log("RIVAAN Backend Status:", data);

        return true;

    } catch (error) {
        console.error("RIVAAN Backend is not reachable:", error);

        return false;
    }
}

// =====================================
// INITIALIZATION
// =====================================

checkBackendConnection();

console.log("RIVAAN Frontend JavaScript Loaded");