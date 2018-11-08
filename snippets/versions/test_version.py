# versions.

versions = ['1.0.0', '1.0.1', '1.0.2']
default_version = '1.0.0'
print(versions)

# alter_versions = []
# for version in versions:
#     if version != default_version:
#         alter_versions.append(version)

arguments_v = '1.0.2'

# print(alter_versions)

update_versions = []
for version in versions:
    if version == default_version and arguments_v == version:
        break
    if version == arguments_v:
        update_versions.append(version)
        break

    if version != default_version:
        update_versions.append(version)


print(update_versions)




# if arguments_v:
#     if arguments_v in alter_versions:
#         for version in alter_versions:
#             if version == arguments_v:


