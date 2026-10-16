
import json
import zipfile
import os

source_model = "food101_model.keras"
patched_model = "food101_model_patched.keras"

if not os.path.exists(source_model):
    raise FileNotFoundError(
        f"Cannot find {source_model} in the current folder."
    )

# Read the saved Keras archive
with zipfile.ZipFile(source_model, "r") as source:
    config = json.loads(source.read("config.json"))

    # Remove the unsupported field wherever it occurs
    def patch_config(obj):
        if isinstance(obj, dict):
            obj.pop("quantization_config", None)

            for value in obj.values():
                patch_config(value)

        elif isinstance(obj, list):
            for item in obj:
                patch_config(item)

    patch_config(config)

    # Write a new archive; keep the original untouched
    with zipfile.ZipFile(
        patched_model, "w", zipfile.ZIP_DEFLATED
    ) as target:

        for item in source.infolist():
            if item.filename == "config.json":
                target.writestr(
                    item,
                    json.dumps(config).encode("utf-8")
                )
            else:
                target.writestr(
                    item,
                    source.read(item.filename)
                )

print("Patched model saved:", patched_model)
print("Original model was not modified.")
